import React from 'react'
import Markdown  from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';

export default function Test() {
    const str = "One of the most famous and influential scientific theories of the 20th century, Albert Einstein's Theory of Relativity is a fundamental concept in modern physics. It consists of two main components: Special Relativity (SR) and General Relativity (GR). \n\n **Special Relativity (SR)**: \n\n In 1905, Einstein introduced SR, which challenged traditional notions of space and time. The key postulates are:\n\n1. **The laws of physics are the same for all observers in uniform motion**: This means that the rules governing physical phenomena, such as the speed of light, remain constant regardless of an observer's relative velocity.\n2. **The speed of light is always constant**: Regardless of the motion of the observer or the source of light, the speed of light remains a universal constant (approximately 299,792,458 meters per second).\n\nFrom these postulates, Einstein derived several consequences:\n\n* **Time dilation**: Time appears to pass slower for an observer in motion relative to a stationary observer.\n* **Length contraction**: Objects appear shorter to an observer in motion relative to a stationary observer.\n* **Relativity of simultaneity**: Two events that are simultaneous for one observer may not be simultaneous for another observer in a different state of motion.\n\n**General Relativity (GR)**:\n\nIn 1915, Einstein expanded SR to include gravity and developed GR. The key postulates are:\n\n1. **The curvature of spacetime is directly related to the presence of mass and energy**: According to GR, massive objects warp spacetime, causing other objects to move along curved trajectories.\n\n2. **The geodesic equation**: This equation describes the shortest path possible in a given spacetime geometry.\n\nFrom these postulates, Einstein derived several consequences:\n\n* **Gravitational redshift**: Light emitted from a source in a strong gravitational field is shifted towards the red end of the spectrum as it escapes.\n* **Gravitational time dilation**: Time passes slower near a massive object due to its stronger gravitational field.\n* **Bending of light around massive objects**: The curvature of spacetime caused by massive objects bends the path of light passing close to them.\n\n**Implications and Applications**:\n\nThe Theory of Relativity has far-reaching implications for our understanding of the universe, including:\n\n* **Cosmology**: GR predicts the expansion of the universe, which is supported by observations of distant galaxies.\n* **Particle physics**: SR explains phenomena such as particle decay and time dilation in high-energy experiments.\n* **Gravitational waves**: The detection of gravitational waves by LIGO and VIRGO have confirmed a key prediction of GR.\n\nIn conclusion, the Theory of Relativity revolutionized our understanding of space, time, and gravity, and has had a profound impact on the development of modern physics."
  return (
        <Markdown
            remarkPlugins={[remarkGfm]}
            // rehypePlugins={[rehypeRaw]}
        >
            {str}
        </Markdown>
  )
}

