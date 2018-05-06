import * as THREE from 'three';
/*
const geometry = new THREE.SphereGeometry(1, 32, 32);
class DataPoint extends THREE.Mesh {
  constructor(radius, x, y, z, color) {
    const material = new THREE.MeshBasicMaterial({ color });

    super(geometry, material);
    this.position.set(x, y, z);
  }
}
// */

class DataPoint extends THREE.Sprite {
  constructor(scale, x, y, z, image) {
    const material = new THREE.SpriteMaterial({
      map: new THREE.TextureLoader().load(image),
    });
    super(material);
    this.position.set(x, y, z);
    this.scale.set(scale, scale, scale);
  }
}
// */

export default DataPoint;
