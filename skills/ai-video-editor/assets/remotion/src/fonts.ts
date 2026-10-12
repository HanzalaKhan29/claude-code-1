import {continueRender, delayRender, staticFile} from 'remotion';

// Load local TTFs before the first frame renders, so text is measured and drawn with the real font
// (a fallback font renders silently and every fitted width is wrong).
const loaded = new Set<string>();

export const loadLocalFont = (family: string, file: string, weight: string) => {
	const key = `${family}-${weight}`;
	if (loaded.has(key) || typeof FontFace === 'undefined') return;
	loaded.add(key);
	const handle = delayRender(`font ${key}`);
	const face = new FontFace(family, `url(${staticFile(file)})`, {weight});
	face
		.load()
		.then((f) => {
			document.fonts.add(f);
			continueRender(handle);
		})
		.catch((err) => {
			console.error(`FONT MISSING ${file}: ${err}`); // read the render log: this means a fallback font
			continueRender(handle);
		});
};
