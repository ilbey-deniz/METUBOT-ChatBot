<template>
    <metubot-chat :enable-did-you-mean-this="enableDidYouMeanThis" :style="fillScreen"/>
</template>

<script>
import MetubotChat from '../components/MetubotChat'

export default {
    name: 'Home',
    props: {
        appBarHeight: Number,
        enableDidYouMeanThis: {
            type: Boolean,
            default() {
                return false;
            }
        }
    },
    components: {
        MetubotChat,
    },
    data() {
        return {
            fillScreen: {
                position: 'fixed',
                top: this.appBarHeight + 'px',
                left: '50%',
                transform: 'translate(-50%)',
                width: '100%',
                height: `calc(100% - ${this.appBarHeight}px)`,
                overflow: 'auto',
            },
        }
    },
}
</script>

<style scoped>


</style>
