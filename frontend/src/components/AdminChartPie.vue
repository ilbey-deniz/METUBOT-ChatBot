<template>
<!--    https://vue-chartjs.org/examples/ -->
    <Pie
            :options="chartOptions"
            :data="data"
    />
</template>

<script>
import { Pie } from 'vue-chartjs'
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    CategoryScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)

export default {
    name: 'AdminChartPie',
    components: { Pie },
    props: {
        data: Object,
    },
    data() {
        return {
            chartOptions: {
                responsive: true
            }
        }
    }
}

</script>

<style scoped>

</style>
