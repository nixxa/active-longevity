/**
 * Dashboard view scripts
 */
define(['jquery', 'highcharts'], function ($, highcharts) {
    'use strict';

    function renderToday(data) {
        Highcharts.chart('container1', {
            chart: {
                type: 'bar'
            },
            title: {
                text: 'По типу мероприятий'
            },
            xAxis: {
                categories: data.chart1.categories
            },
            yAxis: [{
                min: 0,
                title: {
                    text: 'Количество участников'
                }
            }],
            legend: {
                shadow: false
            },
            tooltip: {
                shared: true
            },
            plotOptions: {
                column: {
                    grouping: false,
                    shadow: false,
                    borderWidth: 0
                }
            },
            series: [
                {
                    name: 'План',
                    data: data.chart1.plan,
                    color: 'rgba(126,86,134,.9)'
                },
                {
                    name: 'Факт',
                    data: data.chart1.fact,
                    color: 'rgba(186,60,61,.9)'
                }
            ]
        });

        Highcharts.chart('container2', {
            chart: {
                type: 'column',
                inverted: true,
            },
            title: {
                text: 'Суммарно по округам'
            },
            xAxis: {
                categories: data.chart2.districts
            },
            yAxis: [{
                min: 0,
                title: {
                    text: 'Количество участников'
                },
                
            }],
            legend: {
                shadow: false
            },
            tooltip: {
                shared: true
            },
            plotOptions: {
                column: {
                    stacking: 'normal'
                }
            },
            series: data.chart2.series
        });
    }

    function renderAggregate(data) {
        Highcharts.chart('container3', {
            chart: {
                type: 'bar'
            },
            title: {
                text: 'По типу мероприятий'
            },
            xAxis: {
                categories: [
                    'ОФП',
                    'Гимнастика',
                    'Фитнес, тренажеры',
                    'Скандинавская ходьба',
                    'Танцы',
                    'Пение',
                    'Рисование',
                    'Художественно-прикладное творчество',
                    'Информационные технологии',
                    'Английский язык',
                    'Здорово жить',
                    'Шашки, шахматы'
                ]
            },
            yAxis: [{
                min: 0,
                title: {
                    text: 'Количество участников'
                }
            }],
            legend: {
                shadow: false
            },
            tooltip: {
                shared: true
            },
            plotOptions: {
                column: {
                    grouping: false,
                    shadow: false,
                    borderWidth: 0
                }
            },
            series: [
                {
                    name: 'План',
                    data: [150, 234, 75, 28, 167, 190, 176, 120, 96, 75, 75, 75],
                    color: 'rgba(126,86,134,.9)'
                },
                {
                    name: 'Факт',
                    data: [120, 134, 55, 18, 137, 90, 76, 90, 96, 54, 38, 46],
                    color: 'rgba(186,60,61,.9)'
                }
            ]
        });

        Highcharts.chart('container4', {
            chart: {
                type: 'column',
                inverted: true,
            },
            title: {
                text: 'Суммарно по округам'
            },
            xAxis: {
                categories: [
                    'ЗелАО', 'ЦАО', 'ЗАО', 'СЗАО', 'САО', 'СВАО', 'ВАО', 'ЮВАО', 'ЮАО', 'ЮЗАО'
                ]
            },
            yAxis: [{
                min: 0,
                title: {
                    text: 'Количество участников'
                }
            }],
            legend: {
                shadow: false
            },
            tooltip: {
                shared: true
            },
            plotOptions: {
                column: {
                    stacking: 'normal'
                }
            },
            series: [
                {
                    name: 'ОФП',
                    data: [150, 234, 75, 28, 167, 190, 176, 120, 96, 75],
                    stack: 'v'
                },
                {
                    name: 'Гимнастика',
                    data: [120, 134, 55, 18, 137, 90, 76, 90, 96, 54, 38, 46],
                    stack: 'v'
                },
                {
                    name: 'Фитнес, тренажеры',
                    data: [120, 134, 55, 18, 137, 90, 76, 90, 96, 54, 38, 46],
                    stack: 'v'
                },
                {
                    name: 'Скандинавская ходьба',
                    data: [120, 134, 55, 18, 137, 90, 76, 90, 96, 54, 38, 46],
                    stack: 'v'
                },
                {
                    name: 'Танцы',
                    data: [120, 134, 55, 18, 137, 90, 76, 90, 96, 54, 38, 46],
                    stack: 'v'
                },
                {
                    name: 'Пение',
                    data: [120, 134, 55, 18, 137, 90, 76, 90, 96, 54, 38, 46],
                    stack: 'v'
                },
                {
                    name: 'Художественно-прикладное творчество',
                    data: [120, 134, 55, 18, 137, 90, 76, 90, 96, 54, 38, 46],
                    stack: 'v'
                },
                {
                    name: 'Информационные технологии',
                    data: [120, 134, 55, 18, 137, 90, 76, 90, 96, 54, 38, 46],
                    stack: 'v'
                },
                {
                    name: 'Английский язык',
                    data: [120, 134, 55, 18, 137, 90, 76, 90, 96, 54, 38, 46],
                    stack: 'v'
                },
                {
                    name: 'Здорово жить',
                    data: [120, 134, 55, 18, 137, 90, 76, 90, 96, 54, 38, 46],
                    stack: 'v'
                },
                {
                    name: 'Шашки, шахматы',
                    data: [120, 134, 55, 18, 137, 90, 76, 90, 96, 54, 38, 46],
                    stack: 'v'
                }
            ]
        });
    }

    function onLoad(data) {
        renderToday(data.today);
        //renderAggregate(data.aggregate);        
    }

    return {
        initialize: function (data) {
            $(document).ready(function () {
                onLoad(data);
            });
        }
    }    
});
