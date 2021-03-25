/*
Copyright 2020 XEBIALABS

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

function contributionsSummary(data, bigData, id) {
    var authors = 2;//response['Infrastructure'];
    var committers = 2;//response.data.data.committers;
    var people = "david";//response.data.data.people;
    var dom = document.getElementById(id);
    var chart = echarts.init(dom);
    var option = {
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} Point(s) ({d}%)"
        },
        legend: {
            orient: 'vertical',
            type: 'scroll',
            x: 'left',
            data: ['chad', 'brad', 'todd', 'bill']
        },
        series: [{
                name: 'Complexity Score Small',
                type: 'pie',
                selectedMode: 'single',
                radius: [0, '25%'],
                label: {
                    normal: {
                        show: false
                    }
                },
                data: data
            },
            {
                name: 'Complexity Score Big',
                type: 'pie',
                radius: ['40%', '62.5%'],
                label: {
                    normal: {
                        show: false
                    }
                },
                data: bigData
            }
        ]
    };
    if (option && typeof option === "object") {
        chart.setOption(option, true);
    }
}
