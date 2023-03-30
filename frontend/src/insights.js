import React,{useState,useEffect} from 'react';
import { Pie, Bar, Doughnut } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import SimpleWordcloud from './wordclouds';
import DATA from './services/datalist'
Chart.register(...registerables);

const Insights = () => {
  const dataItems = [
    {
      id: 0,
      name: 'Cobol'
    },
    {
      id: 1,
      name: 'JavaScript'
    },
    {
      id: 2,
      name: 'Basic'
    },
    {
      id: 3,
      name: 'PHP'
    },
    {
      id: 4,
      name: 'Java'
    }
  ]

  const options= {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  const data = {
  labels: [],
  datasets: [
      {
      label: 'Count',
      data: [],
      backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1,
      },
    ],
  };

  const countData = (jsonData) => {
      const counts = {}
      jsonData.forEach((element) => {
          if(counts[element.name]){
              counts[element.name]++
          }
          else{
              counts[element.name] = 1
          }
      });
      const categories = Object.keys(counts);
      const dataCounts = categories.map((category) => counts[category])
      return [categories, dataCounts]
  }

  const [barChartData, setBarChartData] = useState(data);
  const [pieChartData, setPieChartData] = useState(data);
  const [doughChartData, setDoughChartData] = useState(data);
  const [items, setItems] = useState(dataItems)
  const [categories,setCategories] = useState([])
  const [dataCounts,setDataCounts] = useState([])
  const getData = async() => {
    const statsData = await DATA.QueryStatsData()

    return statsData
  }

  useEffect(() => {
    let statsData
    statsData = getData()
    console.log(statsData)
    setDataCounts(statsData['x-val-num-fieldname'])
    setCategories(statsData['x-val-cat-fieldname'])
    console.log(categories)
    console.log(dataCounts)
    setBarChartData({
      ...data,
      labels: categories,
      datasets: [
        {
          ...data.datasets[0],
          data: dataCounts,
        },
      ],
    });

    setPieChartData({
      ...data,
      labels: categories,
      datasets: [
        {
          ...data.datasets[0],
          data: dataCounts,
        },
      ],
    });

    setDoughChartData({
      ...data,
      labels: categories,
      datasets: [
        {
          ...data.datasets[0],
          data: dataCounts,
        },
      ],
    });
  }, [items]);

  return (
    <div>
      <div className='bar_chart_styles'>
        <div style={{ height: '400px', width: '600px' }}>
          <Bar data={barChartData} options={options} />
        </div>
      </div>
      <div className='pie_chart_styles'>
        <div style={{ height: '400px', width: '400px', alignItems: 'center'}}>
          <Pie data={pieChartData} options={options} />
        </div>
        <br/>
        <br/>
        <div style={{ height: '400px', width: '400px', alignItems: 'center' }}>
          <Doughnut data={doughChartData} options={options} />
        </div>
      </div>
      <div className='wordcloud_styles'>
        <SimpleWordcloud/>
      </div>
    </div>
  );
}

export default Insights;