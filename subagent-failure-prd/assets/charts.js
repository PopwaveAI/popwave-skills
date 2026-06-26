(function() {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var accent3 = style.getPropertyValue('--accent3').trim();
  var warn = style.getPropertyValue('--warn').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();

  // --- Chart: 22 runs overview ---
  var chart1 = echarts.init(document.getElementById('chart-overview'), null, { renderer: 'svg' });

  var runIds = [
    '0a0df9f4', '1103b2c5', '196ba3be', '1e41b6f2', '24e9c355',
    '2f43b17c', '3a1eb6aa', '4c1c1257', '55bbd56a', '59425bde',
    '6d28e332', '7f07353f', '80a63265', 'aafbfc36', 'aed2b32b',
    'c3b5ba58', 'c6eb630e', 'c82cc131', 'd66b9011', 'd90fff6e',
    'e8fd8d42', 'ff012ab9'
  ];

  var spawnCounts = [2,2,0,10,0,0,0,0,4,2,0,0,0,0,0,0,0,6,6,0,0,0];
  var yieldCounts = [0,0,0,10,0,0,0,0,4,0,0,0,0,0,0,0,0,8,6,0,0,0];
  var execCounts = [4,0,0,34,6,42,6,0,6,10,2,0,16,2,12,2,0,58,26,0,0,0];

  // Status: 0=normal, 1=silent fail, 2=error fail, 3=intermediate
  var statusData = runIds.map(function(id, i) {
    if (id === '1e41b6f2') return { value: 1, id: id };
    if (id === 'c6eb630e') return { value: 2, id: id };
    if (id === 'c82cc131') return { value: 3, id: id };
    return { value: 0, id: id };
  });

  chart1.setOption({
    backgroundColor: 'transparent',
    title: {
      text: '',
      left: 'center',
      textStyle: { color: ink, fontSize: 14 }
    },
    tooltip: {
      trigger: 'item',
      appendToBody: true,
      formatter: function(params) {
        var idx = params.dataIndex;
        var id = runIds[idx];
        var statusMap = ['正常完成', '静默失败', '401错误', '中间态响应'];
        var s = statusMap[statusData[idx].value];
        return '<b>' + id + '</b><br/>状态: ' + s +
          '<br/>spawn: ' + spawnCounts[idx] +
          '<br/>yield: ' + yieldCounts[idx] +
          '<br/>exec轮询: ' + execCounts[idx];
      }
    },
    legend: {
      data: ['spawn次数', 'yield次数', 'exec轮询次数'],
      top: 0,
      textStyle: { color: muted, fontSize: 11 }
    },
    grid: { top: 40, bottom: 60, left: 50, right: 20 },
    xAxis: {
      type: 'category',
      data: runIds,
      axisLabel: {
        color: muted,
        fontSize: 9,
        rotate: 45,
        interval: 0
      },
      axisLine: { lineStyle: { color: rule } }
    },
    yAxis: {
      type: 'value',
      name: '调用次数',
      nameTextStyle: { color: muted, fontSize: 10 },
      axisLabel: { color: muted, fontSize: 10 },
      splitLine: { lineStyle: { color: rule, type: 'dashed' } }
    },
    series: [
      {
        name: 'spawn次数',
        type: 'bar',
        data: spawnCounts,
        itemStyle: { color: accent },
        animation: false
      },
      {
        name: 'yield次数',
        type: 'bar',
        data: yieldCounts,
        itemStyle: { color: accent3 },
        animation: false
      },
      {
        name: 'exec轮询次数',
        type: 'bar',
        data: execCounts,
        itemStyle: {
          color: function(params) {
            var idx = params.dataIndex;
            if (statusData[idx].value === 1) return accent2; // silent fail = red
            if (statusData[idx].value === 2) return warn; // error = yellow
            if (statusData[idx].value === 3) return warn; // intermediate = yellow
            return muted;
          }
        },
        animation: false
      }
    ]
  });

  window.addEventListener('resize', function() { chart1.resize(); });
})();
