import type {Platform} from './safeZones';

export type Word = {text: string; start: number; end: number};

export type CaptionStyle = {
	enabled: boolean;
	font: string; // family registered in Root (fonts in public/fonts)
	weight: number;
	sizePct: number; // font size as % of frame height (body captions 4.5-5 on 9:16)
	color: string;
	accent: string; // ONE accent: key words and/or the active word
	highlight: 'key' | 'active' | 'both' | 'none';
	maxWords: number; // words per caption group
	yPct: number; // block centre as % of frame height (clamped into the safe zone)
	uppercase: boolean;
	hookUntil: number; // seconds: no captions while a hook title owns the screen
};

export type Graphic =
	| {type: 'title'; at: number; duration: number; text: string; sub?: string}
	| {type: 'stat'; at: number; duration: number; from: number; to: number; prefix?: string; suffix?: string; label?: string}
	| {type: 'image'; at: number; duration: number; src: string; mode: 'push' | 'card'; aspect?: number};

export type EditProps = {
	video: string | null; // file in public/ (the locked cut), or null for pure motion
	durationInSeconds: number | null; // null: last word end + 0.6 s
	width: number;
	height: number;
	fps: number;
	platform: Platform;
	words: Word[]; // words_cut.json (edited timeline)
	keywords: string[]; // chosen by meaning, at most one per caption group
	captions: CaptionStyle;
	graphics: Graphic[];
	texture: 'none' | 'vignette'; // ask the user; grain goes on in grade.py, never twice
	accent: string;
	showSafeZone: boolean; // design aid: draws the zone over the frame (never ship with it on)
	textOnly: boolean; // QA render: transparent, no footage, so safezone.py alpha can audit every text pixel
};
