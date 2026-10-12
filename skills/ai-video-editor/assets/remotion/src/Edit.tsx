import React from 'react';
import {AbsoluteFill, OffthreadVideo, Sequence, staticFile, useVideoConfig} from 'remotion';
import {Captions} from './Captions';
import {GraphicView} from './Graphics';
import {SafeZoneGuide} from './SafeZoneGuide';
import {safeZone} from './safeZones';
import type {EditProps} from './types';

// Layer order, bottom to top: footage, photo push-ins, texture, cards/titles/stats, captions, guide.
// Captions always sit on top of every graphic.
export const Edit: React.FC<EditProps> = (props) => {
	const {fps, width, height} = useVideoConfig();
	const zone = safeZone(props.platform, width, height);
	const seq = (at: number, duration: number) => ({from: Math.round(at * fps), durationInFrames: Math.max(1, Math.round(duration * fps))});
	const photos = props.graphics.filter((g) => g.type === 'image' && g.mode === 'push');
	const overlays = props.graphics.filter((g) => !(g.type === 'image' && g.mode === 'push'));
	return (
		<AbsoluteFill style={{backgroundColor: props.textOnly ? 'transparent' : 'black'}}>
			{props.video && !props.textOnly ? <OffthreadVideo src={staticFile(props.video)} /> : null}
			{props.textOnly ? null : photos.map((g, i) => (
				<Sequence key={`p${i}`} {...seq(g.at, g.duration)} layout="none">
					<GraphicView g={g} zone={zone} font={props.captions.font} accent={props.accent} dur={Math.round(g.duration * fps)} />
				</Sequence>
			))}
			{props.texture === 'vignette' && !props.textOnly ? (
				<AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%)'}} />
			) : null}
			{overlays.map((g, i) => (
				<Sequence key={`g${i}`} {...seq(g.at, g.duration)} layout="none">
					<GraphicView g={g} zone={zone} font={props.captions.font} accent={props.accent} dur={Math.round(g.duration * fps)} />
				</Sequence>
			))}
			<Captions words={props.words} keywords={props.keywords} style={props.captions} zone={zone} />
			{props.showSafeZone && zone ? <SafeZoneGuide zone={zone} /> : null}
		</AbsoluteFill>
	);
};
