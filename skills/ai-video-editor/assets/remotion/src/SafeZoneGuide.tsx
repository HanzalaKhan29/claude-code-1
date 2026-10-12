import React from 'react';
import {AbsoluteFill, useVideoConfig} from 'remotion';
import type {Zone} from './safeZones';

// Design aid only (props.showSafeZone). Dims everything outside the box and paints the button rail red.
export const SafeZoneGuide: React.FC<{zone: Zone}> = ({zone}) => {
	const {width, height} = useVideoConfig();
	const dim = 'rgba(0,0,0,0.45)';
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: 0, top: 0, width, height: zone.y0, background: dim}} />
			<div style={{position: 'absolute', left: 0, top: zone.y1, width, height: height - zone.y1, background: dim}} />
			<div style={{position: 'absolute', left: 0, top: zone.y0, width: zone.x0, height: zone.y1 - zone.y0, background: dim}} />
			<div style={{position: 'absolute', left: zone.x1, top: zone.y0, width: width - zone.x1, height: zone.y1 - zone.y0, background: dim}} />
			<div style={{position: 'absolute', left: zone.railX, top: zone.railY, width: width - zone.railX,
				height: height - zone.railY, background: 'rgba(255,40,40,0.35)'}} />
			<div style={{position: 'absolute', left: zone.x0, top: zone.y0, width: zone.x1 - zone.x0, height: zone.y1 - zone.y0,
				outline: '3px dashed rgba(0,255,140,0.9)'}} />
		</AbsoluteFill>
	);
};
