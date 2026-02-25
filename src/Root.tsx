import "./index.css";
import { Composition } from "remotion";
import { StoryComposition } from "./StoryComposition";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="StoryVideo"
        component={StoryComposition as any}
        durationInFrames={1800} // 60 segundos por padrão
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          image: "https://picsum.photos/1080/1920",
          text: "Título da História",
          audio: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        }}
      />
    </>
  );
};
