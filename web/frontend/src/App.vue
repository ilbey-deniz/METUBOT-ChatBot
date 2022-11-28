<template>
    <v-app>
        <v-app-bar
                app
                elevate-on-scroll

        >
            <div class="d-flex align-center">
                <router-link to="/">
                    <v-img
                            alt="METUBOT Logo"
                            class="mr-2"
                            contain
                            :src="require('./assets/metubot-logo.png')"
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
            <router-view/>
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
        //
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

</style>
