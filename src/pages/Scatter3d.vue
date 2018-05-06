<template>
  <div ref="stage"></div>
</template>

<script>
import * as THREE from 'three';
import Stats from 'stats.js';

import DataPoint from '@/lib/DataPoint';
import Axis from '@/lib/Axis';

const OrbitControls = require('three-orbit-controls')(THREE);

const mnistPCA = require('@/data/mnist_pca.json');

const calcMean = xs => xs.reduce((x, y) => x + y, 0) / xs.length;
const calcStdev = (xs, mean) => xs.reduce((x, y) => x + ((y - mean) ** 2), 0) / xs.length;

const normalize = (vec) => {
  let ret = vec;

  const mean = calcMean(ret);
  const stdev = calcStdev(ret, mean);

  ret = ret.map(x => (x - mean) / stdev);

  const min = Math.min(...ret);
  const max = Math.max(...ret);

  // [0, 1]
  ret = ret.map(v => (v - min) / (max - min));
  // [-1, 1]
  ret = ret.map(x => (2 * x) - 1);

  const centroid = calcMean(ret);

  return ret.map(x => (x - centroid));
};


export default {
  data() {
    const width = 540;
    const height = 540;
    const scene = new THREE.Scene();

    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(width, height);
    renderer.setClearColor(0xF9F9F9, 1.0);

    const camera = new THREE.PerspectiveCamera(45, width / height);
    camera.position.set(80, 80, 80);

    const axisLength = 50;
    scene.add(new Axis('x', axisLength, 0x0000ff));
    scene.add(new Axis('y', axisLength, 0x00ff00));
    scene.add(new Axis('z', axisLength, 0xff0000));


    const controls = new OrbitControls(camera, renderer.domElement);

    const stats = new Stats();

    return {
      scene,
      renderer,
      camera,
      controls,
      stats,
      axisLength,
    };
  },


  mounted() {
    const scale = this.axisLength;

    const vectors = mnistPCA.map(x => x.vector);
    const xs = normalize(vectors.map(v => v[0]));
    const ys = normalize(vectors.map(v => v[1]));
    const zs = normalize(vectors.map(v => v[2]));

    const canvas = document.createElementNS('http://www.w3.org/1999/xhtml', 'canvas');
    canvas.width = 32;
    canvas.height = 32;
    const context = canvas.getContext('2d');

    this.miniIcons = new Image();
    this.miniIcons.src = '/static/mnist_sprite.bmp';
    this.miniIcons.onload = () => {
      mnistPCA.forEach((x, i) => {
        const dx = xs[i] * scale;
        const dy = ys[i] * scale;
        const dz = zs[i] * scale;

        const left = mnistPCA[i].box[0];
        const top = mnistPCA[i].box[1];

        context.clearRect(0, 0, canvas.width, canvas.height);
        context.drawImage(this.miniIcons,
          left, top, 28, 28,
          0, 0, canvas.width, canvas.height);

        this.scene.add(new DataPoint(5, dx, dy, dz, canvas.toDataURL()));
      });
      this.$refs.stage.appendChild(this.renderer.domElement);
      this.$refs.stage.appendChild(this.stats.dom);
      this.animate();
    };
  },

  methods: {

    animate() {
      requestAnimationFrame(this.animate);
      this.stats.begin();
      this.renderer.render(this.scene, this.camera);
      this.stats.end();
    },

  },
};
</script>
