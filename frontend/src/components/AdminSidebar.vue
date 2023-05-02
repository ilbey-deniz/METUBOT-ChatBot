<template>
    <v-sheet class="sheet" color="bg2">
        <aside :class="{'is-expanded': is_expanded}">

            <div class="menu-toggle-wrap">
                <h3 v-if="is_expanded" style="position: relative; top: 0.45rem; font-weight: normal;">
                    Admin Araçları
                </h3>
                <button class="menu-toggle" @click="ToggleMenu">
                    <span class="material-icons">keyboard_double_arrow_right</span>
                </button>
            </div>

            <div class="menu">
                <router-link to="/" class="button">
                    <span class="material-icons">home</span>
                    <span class="text">Metubot Sohbet</span>
                </router-link>
                <router-link to="/yonetim/dashboard" class="button">
                    <span class="material-icons">dashboard</span>
                    <span class="text">Yönetim Paneli</span>
                </router-link>
                <router-link to="/yonetim/tables" class="button">
                    <span class="material-icons">table_chart</span>
                    <span class="text">İstatistik Tablosu</span>
                </router-link>
                <router-link to="/yonetim/charts" class="button">
                    <span class="material-icons">pie_chart</span>
                    <span class="text">Grafikler</span>
                </router-link>
                <router-link to="/yonetim/addquestion" class="button">
                    <span class="material-icons">menu</span>
                    <span class="text">Soru Düzenle</span>
                </router-link>


            </div>
            <div class="flex"></div>

            <div class="menu">
                <router-link to="#" class="button" >
                    <span @click="logout" class="material-icons">logout</span>
                    <span class="text">Çıkış Yap</span>
                </router-link>
                <router-link to="/settings" class="button">
                    <span class="material-icons">settings</span>
                    <span class="text">Ayarlar</span>
                </router-link>
            </div>
        </aside>
    </v-sheet>

</template>


<script setup>

import { ref } from 'vue'
import logoURL from '../assets/metubot-logo-nameless.png'
import router from '@/router';

const is_expanded = ref(localStorage.getItem("is_expanded") === "true")
const ToggleMenu = () => {
    is_expanded.value = !is_expanded.value
    localStorage.setItem("is_expanded", is_expanded.value)
}

const logout = () => {
    sessionStorage.removeItem("token")
    setTimeout(() => {
        router.push("/login")
    }, 500);
}

</script>


<style lang="scss" scoped>


aside {
    display: flex;
    flex-direction: column;
    // background-color: rgb(59, 56, 56);
    color: var(--light);
    // color: wheat;
    width: calc(2rem + 32px);
    overflow: hidden;
    height: 100%;
    padding: 1rem;
    transition: 0.2s ease-in-out;

    .flex {
        flex: 1 1 0%;
    }

    .logo {
        margin-bottom: 1rem;

        img {
            width: 2rem;
        }
    }

    .menu-toggle-wrap {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        transition: 0.2s ease-in-out;

        .menu-toggle {
            transition: 0.2s ease-in-out;

            .material-icons {
                font-size: 2rem;
                color: var(--light);
                // color: wheat;
                transition: 0.2s ease-out;
            }

            &:hover {
                .material-icons {
                    color: var(--primary);
                    // color: red;
                    transform: translateX(0.5rem);
                }
            }
        }
    }

    h3, .button .text {
        opacity: 0;
        transition: opacity 0.3s ease-in-out;
    }

    h3 {


        text-transform: uppercase;
    }

    .menu {
        margin: 0 -1rem;

        .button {
            display: flex;
            align-items: center;
            text-decoration: none;
            transition: 0.2s ease-in-out;
            padding: 0.5rem 1rem;

            .material-icons {
                font-size: 2rem;
                color: var(--light);
                transition: 0.2s ease-in-out;
            }

            .text {
                color: var(--light);
                transition: 0.2s ease-in-out;
            }

            &:hover {
                background-color: var(--dark-alt);

                .material-icons, .text {
                    color: var(--primary);
                }
            }

            &.router-link-exact-active {
                background-color: var(--dark-alt);
                border-right: 5px solid var(--primary);

                .material-icons, .text {
                    color: var(--primary);
                }
            }
        }
    }

    .footer {
        opacity: 0;
        transition: opacity 0.3s ease-in-out;

        p {
            font-size: 0.875rem;
            color: var(--grey);
        }
    }

    &.is-expanded {
        // width: var(--sidebar-width);
        width: var(--sidebar-width);

        .menu-toggle-wrap {
            top: -3rem;

            .menu-toggle {
                transform: rotate(-180deg);
            }
        }

        h3, .button .text {
            opacity: 1;
        }

        .button {
            .material-icons {
                margin-right: 1rem;
            }
        }

        .footer {
            opacity: 0;
        }
    }

    // @media (max-width: 1028px) {
    // 	// position: absolute;
    // 	z-index: 99;
    // }
}

.sheet {
    @media (max-width: 1024px) {
        position: absolute;
        z-index: 100;
        height: 100%;
    }
}
</style>
