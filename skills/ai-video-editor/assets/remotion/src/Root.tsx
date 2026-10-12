import React from 'react';
import {Composition, type CalculateMetadataFunction} from 'remotion';
import {Edit} from './Edit';
import {loadLocalFont} from './fonts';
import type {EditProps} from './types';

// Fonts live in public/fonts (scripts/fetch_fonts.py "Inter:700,900" --dir public/fonts).
loadLocalFont('Inter', 'fonts/Inter-700.ttf', '700');
loadLocalFont('Inter', 'fonts/Inter-900.ttf', '900');

const defaults: EditProps = {
	video: null,
	durationInSeconds: 6,
	width: 1080,
	height: 1920,
	fps: 30,
	platform: 'reels',
	words: [
		{text: 'Replace', start: 0.2, end: 0.6},
		{text: 'these', start: 0.62, end: 0.9},
		{text: 'words', start: 0.92, end: 1.3},
		{text: 'with', start: 1.6, end: 1.8},
		{text: 'words_cut.json.', start: 1.82, end: 2.6},
	],
	keywords: ['words'],
	captions: {enabled: true, font: 'Inter', weight: 900, sizePct: 4.8, color: '#FFFFFF', accent: '#FFD84D',
		highlight: 'key', maxWords: 3, yPct: 62, uppercase: false, hookUntil: 0},
	graphics: [{type: 'title', at: 3, duration: 2.5, text: 'Your title\nlands on its word', sub: 'example graphic'}],
	texture: 'none',
	accent: '#FFD84D',
	showSafeZone: false, // turn on in Studio while designing; a render must never carry it
	textOnly: false,
};

const calculateMetadata: CalculateMetadataFunction<EditProps> = ({props}) => {
	const lastWord = props.words.length ? props.words[props.words.length - 1].end + 0.6 : 5;
	const seconds = props.durationInSeconds ?? lastWord;
	return {durationInFrames: Math.max(1, Math.ceil(seconds * props.fps)), fps: props.fps, width: props.width, height: props.height};
};

export const RemotionRoot: React.FC = () => (
	<Composition id="Edit" component={Edit} defaultProps={defaults} calculateMetadata={calculateMetadata}
		durationInFrames={180} fps={30} width={1080} height={1920} />
);
