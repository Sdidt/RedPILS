import { Pie, Bar, Doughnut } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import SimpleWordcloud from './wordclouds';
import React, { useEffect, useState } from 'react';
import { defaultCallbacks } from 'react-wordcloud';
import Typography from '@mui/material/Typography';
import { NumericFormat } from 'react-number-format';
import NoResultsImg from "./pic1.png";
Chart.register(...registerables);

const InsightsComp = (props) => {
    let barChartData = props.barChartData
    let pieChartData = props.pieChartData
    let doughChartData = props.doughChartData
    let statsCheck = props.statsCheck
    let avgRedditScore = props.avgRedditScore
    let avgScore = props.avgScore
    let searchTime = props.searchTime

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
                <div className='numberMetricsDiv'>
                    <div className='numericIndvDiv'>
                        <Typography variant="h4" gutterBottom style={{color:'white'}}>
                            Query Speed (sec)
                        </Typography>
                        <Typography variant="h1" gutterBottom style={{color:'rgb(0, 255, 0)'}}>
                            {searchTime.toFixed(2)}
                        </Typography>
                    </div>
                    <div class="vl"></div>
                    <div className='numericIndvDiv'>
                        <Typography variant="h4" gutterBottom style={{color:'white'}}>
                            Average Reddit Score
                        </Typography>
                        <Typography variant="h1" gutterBottom style={{color:'rgb(0, 255, 0)'}}>
                            {avgRedditScore.toFixed(2)}
                        </Typography>
                    </div>
                    <div class="vl"></div>
                    <div className='numericIndvDiv'>
                        <Typography variant="h4" gutterBottom style={{color:'white'}}>
                            Average Score
                        </Typography>
                        <Typography variant="h1" gutterBottom style={{color:'rgb(0, 255, 0)'}}>
                            {avgScore.toFixed(2)}
                        </Typography>
                    </div>
                </div>
                <div className='bar_chart_styles'>
                    <div style={{ height: '400px', width: '600px' }}>
                    <Bar data={barChartData} options={options} />
                    </div>
                </div>
                <div className='pie_chart_styles'>
                    <div style={{ height: '400px', width: '400px', alignItems: 'center',padding:"2%"}}>
                    <Pie data={pieChartData} options={options} />
                    </div>
                    <div style={{ height: '400px', width: '400px', alignItems: 'center',padding:"2%"}}>
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