// Remotion CLI config. Keep frames as JPEG for speed; the QA text-only render switches to PNG on the CLI.
import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
Config.setConcurrency(null); // let Remotion pick from the CPU count
