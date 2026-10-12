// Same numbers as scripts/_common.py SAFE_ZONES (1080x1920 basis, scaled to the composition).
// box = x0, y0, x1, y1 where text may live; rail = the button column (x > railX for y > railY) to stay out of.
export type Platform = 'reels' | 'reels-ad' | 'tiktok' | 'shorts' | 'cross';

const BASE: Record<Platform, {box: [number, number, number, number]; railX: number; railY: number}> = {
	reels: {box: [35, 220, 1045, 1500], railX: 950, railY: 1340}, // user's organic Instagram spec
	'reels-ad': {box: [65, 269, 1015, 1248], railX: 950, railY: 1100},
	tiktok: {box: [120, 240, 960, 1260], railX: 780, railY: 840},
	shorts: {box: [48, 288, 888, 1248], railX: 888, railY: 700},
	cross: {box: [120, 288, 888, 1248], railX: 780, railY: 840},
};

export type Zone = {x0: number; y0: number; x1: number; y1: number; railX: number; railY: number};

export const safeZone = (platform: Platform, width: number, height: number): Zone | null => {
	if (height <= width) return null; // safe zones are a 9:16 concern
	const sx = width / 1080;
	const sy = height / 1920;
	const z = BASE[platform] ?? BASE.cross;
	return {
		x0: z.box[0] * sx, y0: z.box[1] * sy, x1: z.box[2] * sx, y1: z.box[3] * sy,
		railX: z.railX * sx, railY: z.railY * sy,
	};
};

// Widest box, centred on the frame, that a block can use at vertical band [top, bottom] without touching the rail.
export const centredWidthAt = (zone: Zone, width: number, top: number, bottom: number): number => {
	const right = bottom > zone.railY ? Math.min(zone.x1, zone.railX) : zone.x1;
	const half = Math.min(width / 2 - zone.x0, right - width / 2);
	return Math.max(0, 2 * half);
};
