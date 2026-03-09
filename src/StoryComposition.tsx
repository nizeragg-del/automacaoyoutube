import React from "react";
import {
    AbsoluteFill,
    Audio,
    Img,
    interpolate,
    useCurrentFrame,
    useVideoConfig,
    staticFile,
    spring,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { Subtitles } from "./components/Subtitles";
import { AudioVisualizer } from "./components/AudioVisualizer";
import { Caption } from "@remotion/captions";
import { useWindowedAudioData, visualizeAudio } from "@remotion/media-utils";

interface StoryData {
    images: string[];
    text: string;
    audio: string;
    subtitles?: Caption[];
}

export const StoryComposition: React.FC<StoryData> = ({ images, text, audio, subtitles }) => {
    const frame = useCurrentFrame();
    const { durationInFrames, fps } = useVideoConfig();

    // 1. Audio Analysis for Bass Bump
    const audioSrc = audio.startsWith("http") ? audio : staticFile(audio);
    const audioData = useWindowedAudioData({
        src: audioSrc,
        frame,
        fps,
        windowInSeconds: 0.1,
    });

    let bassIntensity = 0;
    if (audioData && audioData.audioData) {
        const frequencies = visualizeAudio({
            fps,
            frame,
            audioData: audioData.audioData,
            numberOfSamples: 64,
        });
        const lowFreqs = frequencies.slice(0, 8); // Deep bass
        bassIntensity = lowFreqs.reduce((acc, v) => acc + v, 0) / lowFreqs.length;
    }

    // 2. Logic for Transitions
    const validImages = Array.isArray(images) && images.length > 0 ? images : [staticFile("placeholder.jpg")];
    const transitionDuration = Math.floor(fps * 0.8); // 0.8s transition
    const totalTransitionsDuration = transitionDuration * (validImages.length - 1);
    const availableFrames = durationInFrames + totalTransitionsDuration;
    const framesPerImage = Math.floor(availableFrames / validImages.length);

    // Headline Animation
    const headlineEntrance = spring({
        frame,
        fps,
        config: { damping: 12 },
        durationInFrames: 30,
    });

    return (
        <AbsoluteFill style={{
            backgroundColor: "white",
            transform: `scale(${1 + bassIntensity * 0.03})`, // Subtle bass bump
        }}>
            <TransitionSeries>
                {validImages.map((src, index) => (
                    <React.Fragment key={`fragment-${index}`}>
                        <TransitionSeries.Sequence durationInFrames={framesPerImage}>
                            <AbsoluteFill>
                                <Img
                                    src={src.startsWith("http") ? src : staticFile(src)}
                                    style={{
                                        width: "100%",
                                        height: "100%",
                                        objectFit: "cover",
                                        // Subtle internal pan motion
                                        transform: `scale(1.1) translate(${(index % 2 === 0 ? 1 : -1) * (frame / 20)}px, 0px)`,
                                    }}
                                />
                            </AbsoluteFill>
                        </TransitionSeries.Sequence>
                        {index < validImages.length - 1 && (
                            <TransitionSeries.Transition
                                presentation={fade()}
                                timing={linearTiming({ durationInFrames: transitionDuration })}
                            />
                        )}
                    </React.Fragment>
                ))}
            </TransitionSeries>

            {/* Audio Visualization Layer */}
            <AudioVisualizer audioSrc={audioSrc} />

            {/* Legendas Dinâmicas */}
            <Subtitles audioFile={audio} subtitles={subtitles} />

            {/* Headline Profissional */}
            <AbsoluteFill style={{
                top: "8%",
                height: "15%",
                justifyContent: "center",
                alignItems: "center",
                padding: "0 50px",
                opacity: headlineEntrance,
                transform: `translateY(${interpolate(headlineEntrance, [0, 1], [20, 0])}px)`
            }}>
                <h1 style={{
                    color: "white",
                    fontSize: 52,
                    fontWeight: 900,
                    textTransform: "uppercase",
                    textAlign: "center",
                    fontFamily: "Inter, sans-serif",
                    textShadow: "0px 10px 30px rgba(0,0,0,0.8), 4px 4px 0px #000",
                    margin: 0,
                    letterSpacing: "2px",
                    lineHeight: 1.1
                }}>
                    {text}
                </h1>
            </AbsoluteFill>

            {/* Polimento: Vinheta e Ruído */}
            <AbsoluteFill
                style={{
                    background: "radial-gradient(circle, rgba(0,0,0,0) 30%, rgba(0,0,0,0.9) 100%)",
                    pointerEvents: "none",
                    zIndex: 1000
                }}
            />

            <AbsoluteFill
                style={{
                    backgroundImage: `url("https://www.transparenttextures.com/patterns/real-carbon-fibre.png")`,
                    opacity: 0.05,
                    mixBlendMode: "overlay",
                    pointerEvents: "none",
                    zIndex: 1001
                }}
            />

            <Audio src={audioSrc} />
        </AbsoluteFill>
    );
};
