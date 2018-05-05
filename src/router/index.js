import Vue from 'vue';
import Router from 'vue-router';
import Scatter3d from '@/pages/Scatter3d';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Scatter3d',
      component: Scatter3d,
    },
  ],
});
