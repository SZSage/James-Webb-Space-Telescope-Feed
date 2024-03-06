import * as THREE from 'three';
import { useEffect } from 'react';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import './Model.css';
import SceneInit from './Sceneinit';
import Footer from './Footer';

/**
 RenderView.jsx is the file that is in charge of rendering the 3D model of the James Webb Telescope which offeres the users an interactive model
 in which they can move around and zoom in on to see what the James Webb Telescope looks like. Its addition is for a purly educational feature
 and is a static model that is rendered
 */

function RenderView () {
  useEffect(() => {
    const test = new SceneInit('myThreeJsCanvas');
    test.initialize();
    test.animate();

    // const boxGeometry = new THREE.BoxGeometry(8, 8, 8);
    // const boxMaterial = new THREE.MeshNormalMaterial();
    // const boxMesh = new THREE.Mesh(boxGeometry, boxMaterial);
    // test.scene.add(boxMesh);

    let loadedModel;
    const glftLoader = new GLTFLoader();
    glftLoader.load('/3d-JSWT/scene.gltf', (gltfScene) => {
      loadedModel = gltfScene;
      // console.log(loadedModel);

      gltfScene.scene.rotation.y = Math.PI / 8;
      gltfScene.scene.position.y = 3;
      gltfScene.scene.scale.set(10, 10, 10);
      test.scene.add(gltfScene.scene);
    });

  }, []);

  return (
    <>
    <div className='model'>
      <canvas id="myThreeJsCanvas" />
    </div>
    <Footer/>
    </>
  );
}

export default RenderView;
