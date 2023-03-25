<template>
    <v-app :style="{background: $vuetify.theme.themes[theme].background}">
        <v-app-bar
                app
                elevation="4"
                :height="appBarHeight"
                style="position: absolute"

        >
            <div class="d-flex align-center">
                <router-link to="/">
                    <v-img
                            alt="METUBOT Logo"
                            class="mr-2"
                            contain
                            :src="require('@/assets/metubot-logo.png')"
                            transition="scale-transition"
                            width="166"
                    />
                </router-link>

            </div>
            <v-toolbar-title class="text-h5" v-if="$route.name === 'admin'">Yönetim</v-toolbar-title>


            <v-spacer></v-spacer>
            <router-link class="mr-2 grey--text text-decoration-none" to="/yonetim">Yönetim</router-link>
            <router-link class="mr-2 grey--text text-decoration-none" to="/">Metubot</router-link>
            <v-icon v-if="$vuetify.theme.dark" @click="setDarkMode(false)">
                mdi-weather-sunny
            </v-icon>
            <v-icon v-else @click="setDarkMode(true)">
                mdi-weather-night
            </v-icon>

        </v-app-bar>

        <v-main>

            <router-view :app-bar-height="appBarHeight"/>
        </v-main>
    </v-app>
</template>

<script>

export default {
    name: 'App',
    watch: {
        $route: {
            immediate: true,
            handler(to, from) {
                document.title = to.meta.title || 'METUBOT'
            },
        },
    },
    data: () => ({
        appBarHeight: 64,
    }),
    computed: {
        theme() {
            return (this.$vuetify.theme.dark) ? 'dark' : 'light'
        },
    },
    mounted() {
        // load dark mode from local storage
        this.$vuetify.theme.dark = localStorage.getItem('darkMode') === 'true';
    },
    methods: {
        setDarkMode(darkMode) {
            this.$vuetify.theme.dark = darkMode;
            localStorage.setItem('darkMode', darkMode ? 'true' : 'false');
        }
    }
};
</script>

<style>
html {
    overflow-y: auto !important;
}

* {
    box-sizing: border-box;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity .5s
}

.fade-enter,
.fade-leave-to {
    opacity: 0
}

.light-scrollbar::-webkit-scrollbar {
    width: 15px;
}

.light-scrollbar::-webkit-scrollbar-track {
    background: #e6e6e6;
    border-left: 1px solid #dadada;
}

.light-scrollbar::-webkit-scrollbar-thumb {
    background: #b0b0b0;
    border: solid 3px #e6e6e6;
    border-radius: 7px;
}

.light-scrollbar::-webkit-scrollbar-thumb:hover {
    background: black;
}

.dark-scrollbar::-webkit-scrollbar {
    width: 15px;
}

.dark-scrollbar::-webkit-scrollbar-track {
    background: #202020;
    border-left: 1px solid #2c2c2c;
}

.dark-scrollbar::-webkit-scrollbar-thumb {
    background: #3e3e3e;
    border: solid 3px #202020;
    border-radius: 7px;
}

.dark-scrollbar::-webkit-scrollbar-thumb:hover {
    background: white;
}
</style>
