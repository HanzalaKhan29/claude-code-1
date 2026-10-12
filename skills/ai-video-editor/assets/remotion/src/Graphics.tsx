import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {fitText} from '@remotion/layout-utils';
import type {Graphic} from './types';
import {centredWidthAt, type Zone} from './safeZones';

// Every graphic lives inside its own <Sequence>, so frame 0 here is the spoken word it lands on.
// Entrances decelerate, exits are faster, nothing idles. The whole graphic leaves 0.2 s before its end.
const useEnterExit = (durationInFrames: number) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const enter = spring({frame, fps, config: {damping: 200, mass: 0.6}});
	const exit = interpolate(frame, [durationInFrames - Math.round(0.25 * fps), durationInFrames - Math.round(0.05 * fps)],
		[1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.cubic)});
	return {frame, fps, enter, exit};
};

const Title: React.FC<{g: Extract<Graphic, {type: 'title'}>; zone: Zone | null; font: string; accent: string; dur: number}> = ({
	g, zone, font, dur,
}) => {
	const {width, height} = useVideoConfig();
	const {enter, exit} = useEnterExit(dur);
	const top = zone ? zone.y0 + (zone.y1 - zone.y0) * 0.08 : height * 0.12;
	const maxW = (zone ? centredWidthAt(zone, width, top, top + height * 0.2) : width * 0.86) - 8;
	const lines = g.text.split('\n');
	const longest = lines.reduce((a, l) => (l.length > a.length ? l : a), '');
	const fs = Math.min(height * 0.065, fitText({text: longest, withinWidth: maxW, fontFamily: font, fontWeight: 900}).fontSize);
	return (
		<div style={{position: 'absolute', left: (width - maxW) / 2, width: maxW, top, textAlign: 'center',
			opacity: Math.min(enter, exit), transform: `translateY(${(1 - enter) * 40}px)`}}>
			{lines.map((l, i) => (
				<div key={i} style={{fontFamily: font, fontWeight: 900, fontSize: fs, lineHeight: 1.05, color: 'white',
					letterSpacing: '-0.02em', textShadow: '0 4px 24px rgba(0,0,0,0.5)'}}>{l}</div>
			))}
			{g.sub ? (
				<div style={{fontFamily: font, fontWeight: 700, fontSize: fs * 0.38, color: 'rgba(255,255,255,0.85)', marginTop: fs * 0.2}}>
					{g.sub}
				</div>
			) : null}
		</div>
	);
};

const Stat: React.FC<{g: Extract<Graphic, {type: 'stat'}>; zone: Zone | null; font: string; accent: string; dur: number}> = ({
	g, zone, font, accent, dur,
}) => {
	const {width, height} = useVideoConfig();
	const {frame, fps, enter, exit} = useEnterExit(dur);
	// Seek-safe: the number is a pure function of the frame, never accumulated.
	const v = interpolate(frame, [0, Math.round(0.9 * fps)], [g.from, g.to], {
		extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
	const text = `${g.prefix ?? ''}${Math.round(v).toLocaleString('en-US')}${g.suffix ?? ''}`;
	const finalText = `${g.prefix ?? ''}${Math.round(g.to).toLocaleString('en-US')}${g.suffix ?? ''}`;
	const top = zone ? zone.y0 + (zone.y1 - zone.y0) * 0.1 : height * 0.15;
	const maxW = (zone ? centredWidthAt(zone, width, top, top + height * 0.2) : width * 0.86) - 8;
	const fs = Math.min(height * 0.11, fitText({text: finalText, withinWidth: maxW, fontFamily: font, fontWeight: 900,
		fontVariantNumeric: 'tabular-nums'}).fontSize);
	return (
		<div style={{position: 'absolute', left: (width - maxW) / 2, width: maxW, top, textAlign: 'center',
			opacity: Math.min(enter, exit), transform: `scale(${0.92 + 0.08 * enter})`}}>
			<div style={{fontFamily: font, fontWeight: 900, fontSize: fs, color: accent, lineHeight: 1,
				fontVariantNumeric: 'tabular-nums'}}>{text}</div>
			{g.label ? <div style={{fontFamily: font, fontWeight: 700, fontSize: fs * 0.3, color: 'white', marginTop: fs * 0.12}}>{g.label}</div> : null}
		</div>
	);
};

const Photo: React.FC<{g: Extract<Graphic, {type: 'image'}>; zone: Zone | null; dur: number}> = ({g, zone, dur}) => {
	const {width, height} = useVideoConfig();
	const {frame, enter, exit} = useEnterExit(dur);
	if (g.mode === 'push') {
		const scale = interpolate(frame, [0, dur], [1.0, 1.08]);
		return (
			<AbsoluteFill style={{opacity: exit}}>
				<Img src={staticFile(g.src)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${scale})`}} />
			</AbsoluteFill>
		);
	}
	// Card size: as large as possible while the WHOLE card (border included) stays inside the zone and off the rail.
	const aspect = g.aspect ?? 4 / 3;
	const border = 14;
	const shadowPad = 40; // the drop shadow is part of the graphic: it stays out of the rail as well
	const top = zone ? zone.y0 + (zone.y1 - zone.y0) * 0.08 : height * 0.15;
	let outer = width * 0.7;
	if (zone) {
		const full = Math.min(zone.x1 - zone.x0, 2 * (zone.x1 - width / 2), 2 * (width / 2 - zone.x0)) * 0.94;
		const clearRail = 2 * (zone.railX - width / 2 - shadowPad); // narrow enough to pass beside the rail
		const fitH = (bottom: number) => (bottom - top - 2 * border) * aspect + 2 * border; // outer width ending at bottom
		const aboveRail = Math.min(full, fitH(zone.railY - shadowPad)); // wide, but must end above the rail
		const besideRail = Math.min(full, clearRail, fitH(zone.y1 - shadowPad)); // narrow, may run down to the box bottom
		outer = Math.max(aboveRail, besideRail);
	}
	const boxW = outer - 2 * border; // image width inside the border
	return (
		<div style={{position: 'absolute', left: (width - outer) / 2, top, width: boxW, opacity: Math.min(enter, exit),
			transform: `scale(${0.9 + 0.1 * enter}) rotate(${(1 - enter) * -3}deg)`, border: `${border}px solid white`,
			boxShadow: '0 10px 28px rgba(0,0,0,0.35)', background: 'white', boxSizing: 'content-box'}}>
			<Img src={staticFile(g.src)} style={{width: '100%', height: boxW / aspect, objectFit: 'cover', display: 'block'}} />
		</div>
	);
};

export const GraphicView: React.FC<{g: Graphic; zone: Zone | null; font: string; accent: string; dur: number}> = (p) => {
	if (p.g.type === 'title') return <Title {...p} g={p.g} />;
	if (p.g.type === 'stat') return <Stat {...p} g={p.g} />;
	return <Photo g={p.g} zone={p.zone} dur={p.dur} />;
};
