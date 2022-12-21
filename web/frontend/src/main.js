import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';

Vue.config.productionTip = false
Vue.use(Vuetify);

import colors from 'vuetify/lib/util/colors'



new Vue({
    router,
    vuetify: new Vuetify({
        theme: {
            dark: false,
            themes: {
                light: {
                    background: '#f5f0f1', // Not automatically applied
                    bg2: '#64748b',
                },
                dark: {
                    bg2: '#2c2a2a',
                }

            },
        },
    }),
    render: h => h(App),
}).$mount('#app')
