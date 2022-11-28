<template>
    <v-app>
        <v-app-bar
                app
                elevation="4"
                :height="appBarHeight"

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

            <v-spacer></v-spacer>
            <router-link class="mr-2 grey--text text-decoration-none" to="admin">Yönetim</router-link>
            <v-icon v-if="$vuetify.theme.dark"
                    @click="$vuetify.theme.dark = false"
            >
                mdi-weather-sunny
            </v-icon>
            <v-icon v-else
                    @click="$vuetify.theme.dark = true"
            >
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
};
</script>

<style>
html {
    overflow-y: auto !important;
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
