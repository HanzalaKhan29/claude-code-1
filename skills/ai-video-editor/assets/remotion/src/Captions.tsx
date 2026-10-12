import React, {useMemo} from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {fitText, measureText} from '@remotion/layout-utils';
import type {CaptionStyle, Word} from './types';
import {centredWidthAt, type Zone} from './safeZones';

const clean = (w: string) => w.toLowerCase().replace(/[^\p{L}\p{N}']/gu, '');

// Break groups at pauses >= 250 ms, sentence ends and the word limit; never span a breath.
export const groupWords = (words: Word[], maxWords: number): Word[][] => {
	const groups: Word[][] = [];
	let cur: Word[] = [];
	words.forEach((w, i) => {
		cur.push(w);
		const next = words[i + 1];
		const sentenceEnd = /[.!?]$/.test(w.text);
		if (!next || sentenceEnd || cur.length >= maxWords || next.start - w.end >= 0.25) {
			groups.push(cur);
			cur = [];
		}
	});
	return groups;
};

export const Captions: React.FC<{words: Word[]; keywords: string[]; style: CaptionStyle; zone: Zone | null}> = ({
	words,
	keywords,
	style,
	zone,
}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const t = frame / fps;
	const groups = useMemo(() => groupWords(words, style.maxWords), [words, style.maxWords]);
	const keys = useMemo(() => new Set(keywords.map(clean)), [keywords]);

	if (!style.enabled || t < style.hookUntil) return null;
	const gi = groups.findIndex((g, i) => {
		const enter = g[0].start - 0.05;
		const nextStart = groups[i + 1]?.[0].start ?? Infinity;
		const leave = Math.min(g[g.length - 1].end + 0.5, nextStart - 0.05);
		return t >= enter && t < leave;
	});
	if (gi < 0) return null;
	const group = groups[gi];

	const base = (style.sizePct / 100) * height;
	const lineH = 1.12;
	const pad = 14; // the text shadow reaches ~12 px past the glyphs: keep it inside the zone too
	const shown = group.map((w) => (style.uppercase ? w.text.toUpperCase() : w.text));
	// Greedy wrap with real glyph widths, so the block height is known BEFORE it is placed.
	const linesAt = (fs: number, maxW: number) => {
		const space = measureText({text: ' ', fontFamily: style.font, fontWeight: style.weight, fontSize: fs}).width;
		let lines = 1;
		let x = 0;
		for (const w of shown) {
			const ww = measureText({text: w, fontFamily: style.font, fontWeight: style.weight, fontSize: fs}).width;
			if (x > 0 && x + space + ww > maxW) {
				lines += 1;
				x = ww;
			} else {
				x += (x > 0 ? space : 0) + ww;
			}
		}
		return lines;
	};
	const place = (fs: number) => {
		let centreY = (style.yPct / 100) * height;
		let maxW = width * 0.84;
		let lines = linesAt(fs, maxW);
		for (let pass = 0; pass < 3 && zone; pass++) {
			const half = (lines * fs * lineH) / 2;
			centreY = Math.min(Math.max(centreY, zone.y0 + half + pad), zone.y1 - half - pad);
			maxW = centredWidthAt(zone, width, centreY - half - pad, centreY + half + pad) - 2 * pad;
			lines = linesAt(fs, maxW);
		}
		return {centreY, maxW, lines};
	};
	// At most 2 lines: shrink up to 30%, then accept what fits (a long single word is fitted on its own).
	let fontSize = base;
	let layout = place(fontSize);
	while (layout.lines > 2 && fontSize > base * 0.7) {
		fontSize *= 0.94;
		layout = place(fontSize);
	}
	const longest = shown.reduce((a, w) => (w.length > a.length ? w : a), '');
	fontSize = Math.min(fontSize, fitText({text: longest, withinWidth: layout.maxW, fontFamily: style.font,
		fontWeight: style.weight}).fontSize);
	const {centreY, maxW} = place(fontSize);

	return (
		<AbsoluteFill>
			<div
				style={{
					position: 'absolute',
					left: (width - maxW) / 2,
					width: maxW,
					top: centreY,
					transform: 'translateY(-50%)',
					textAlign: 'center',
					fontFamily: style.font,
					fontWeight: style.weight,
					fontSize,
					lineHeight: lineH,
					color: style.color,
					textTransform: style.uppercase ? 'uppercase' : 'none',
					textShadow: '0 2px 10px rgba(0,0,0,0.55), 0 0 2px rgba(0,0,0,0.9)',
				}}
			>
				{group.map((w, i) => {
					const next = group[i + 1];
					const active = t >= w.start && t < (next ? next.start : w.end + 0.5);
					const isKey = keys.has(clean(w.text));
					const lit =
						(style.highlight === 'key' && isKey) ||
						(style.highlight === 'active' && active) ||
						(style.highlight === 'both' && (isKey || active));
					return (
						<span key={i} style={{color: lit ? style.accent : style.color}}>
							{w.text}
							{i < group.length - 1 ? ' ' : ''}
						</span>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};
