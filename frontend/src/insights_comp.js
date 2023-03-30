import { Pie, Bar, Doughnut } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import SimpleWordcloud from './wordclouds';
import React, { useEffect, useState } from 'react';
import { defaultCallbacks } from 'react-wordcloud';
import NoResultsImg from "./pic1.png";
Chart.register(...registerables);

const InsightsComp = (props) => {
    let barChartData = props.barChartData
    let pieChartData = props.pieChartData
    let doughChartData = props.doughChartData
    let statsCheck = props.statsCheck

    console.log(barChartData)

    const options= {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      };

    return (
        <div>
            {statsCheck > 0 ? (
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
                {/* <div className='wordcloud_styles'>
                    <SimpleWordcloud/>
                </div> */}
            </div> ) : (
        <div>
        <div className='NoResultsDiv'>
          Nothing to display here. Search for a term or click on commonly search terms to see more results.
        </div> 
        <div className='NoResultsImg'>
          <img src = {NoResultsImg} alt="NoResultImg" className="about-img" style={{width:"40%",height:"40%"}}></img>
        </div>
        </div>
        )
    }
        </div>
    )
}

export default InsightsComp;