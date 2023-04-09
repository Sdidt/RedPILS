import { Pie, Bar, Doughnut, Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import React, { useEffect, useState } from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import Plot from 'react-plotly.js';
import NoResultsImg from "./pic1.png";
import wordCloudImg from "./query_wordcloud.png"
import DATA from "./services/datalist"
Chart.register(...registerables);

const InsightsComp = (props) => {
    const [polaritySelect, setPolaritySelect] = useState('All');
    const [geoplotSelect, setGeoPlotSelect] = useState("num_results");
    const [geoPlotDataVar, setGeoPlotDataVar] = useState(props.geoPlotData)
    const [polarWordCloudDataLink, setPolarWordCloudDataLink] = useState(props.polarWordCloudData)

    let wordCloudData = props.wordCloudData
    let barChartDataScore = props.barChartDataScore
    let barChartDataCount = props.barChartDataCount
    let pieChartData = props.pieChartData
    let doughChartData = props.doughChartData
    let timeChartData = props.timeChartData
    let timeNoResults = props.timeNoResults
    let timePolarityData = props.timePolarityData
    let statsCheck = props.statsCheck
    let avgRedditScore = props.avgRedditScore
    let avgScore = props.avgScore
    let searchTime = props.searchTime
    let geoPlotData = props.geoPlotData
    let polarWordCloudData = props.polarWordCloudData

    console.log(timeChartData)

    const options= {
        scales: {
          y: {
            beginAtZero: true,
            color:"white",
            ticks: {
                color: 'white', // change x axis label color here
              },
          },
          x: {
            ticks: {
                color: 'white', // change x axis label color here
              },
          }
        },
        plugins: {
            legend: {
              labels: {
                color: 'white' // set legend labels color
              }
            }
        }
      };

    const timeoptions = {
        responsive: true,
        scales:{
            x: {
                ticks: {
                    color: 'white', // change x axis label color here
                  },
              },
            y: {
                ticks: {
                    color: 'white', // change x axis label color here
                  },
              }
        },
        plugins: {
          legend: {
            position: 'top',
            labels: {
                color: 'white' // set legend labels color
              }
          },
          title: {
            display: true,
            text: 'Time ',
          },
        },
    };

    const handleChange = (event: SelectChangeEvent) => {
        setPolaritySelect(event.target.value)
        let polarWordCloudData = props.polarWordCloudData+"&polarity="+event.target.value
        setPolarWordCloudDataLink(polarWordCloudData)
        console.log(polarWordCloudData)
    }

    const handleGeoSelect = async(event: SelectChangeEvent) => {
        setGeoPlotSelect(event.target.value)
        if(event.target.value != 'num_results'){
            var dummy_geoplot_data = await DATA.QueryGeoPlotData(event.target.value,'rdylbu')
            setGeoPlotDataVar(dummy_geoplot_data)
        }
        else{
            var dummy_geoplot_data = await DATA.QueryGeoPlotData(event.target.value,'Blues')
            setGeoPlotDataVar(dummy_geoplot_data)
        }
    }

    useEffect(() => {
        setPolarWordCloudDataLink(polarWordCloudData)
      }, [polarWordCloudData]);

    return (
        <div>
            {statsCheck > 0 ? (
            <div>
                <div className='numberMetricsDiv'>
                    <div className='numericIndvDiv'>
                        <Typography variant="h5" gutterBottom style={{color:'white',height:"55px",width:"100%"}}>
                            Query Speed
                        </Typography>
                        <Typography variant="h1" gutterBottom style={{color:'rgb(0, 255, 0)'}}>
                            {searchTime.toFixed(2)}
                        </Typography>
                    </div>
                    <div class="vl"></div>
                    <div className='numericIndvDiv'>
                        <Typography variant="h5" gutterBottom style={{color:'white',height:"55px",width:"100%"}}>
                            Average Reddit Score
                        </Typography>
                        <Typography variant="h1" gutterBottom style={{color:'rgb(0, 255, 0)'}}>
                            {avgRedditScore.toFixed(2)}
                        </Typography>
                    </div>
                    <div class="vl"></div>
                    <div className='numericIndvDiv'>
                        <Typography variant="h5" gutterBottom style={{color:'white',height:"55px",width:"100%"}}>
                            Avg Weighted Score
                        </Typography>
                        <Typography variant="h1" gutterBottom style={{color:'rgb(0, 255, 0)'}}>
                            {avgScore.toFixed(2)}
                        </Typography>
                    </div>
                </div>
                <div className='bar_chart_styles'>
                    <div style={{ height: '400px', width: '600px' ,color:"white"}}>
                    <Bar data={barChartDataScore} options={options} />
                    </div>
                    <div style={{ height: '400px', width: '600px' ,color:"white"}}>
                    <Bar data={barChartDataCount} options={options} />
                    </div>
                </div>
                <Typography variant="h3" gutterBottom style={{color:'Orange',height:"55px",width:"100%",backgroundColor:"black"}}>
                    Query Specific Data Insights
                </Typography>
                <br></br>
                <div className='wordcloud_styles'>
                    <img src={wordCloudData} alt="wordcloud" />
                    {/* <FormControl fullWidth sx={{ m: 1, width:"100%"}}>
                    <InputLabel id="demo-simple-select-label">Polarity</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={polaritySelect}
                        label="Polarity"
                        onChange={handleChange}
                        sx={{ m: 1, backgroundColor:'white'}}
                    >
                        <MenuItem value={"All"}>All</MenuItem>
                        <MenuItem value={"left"}>Left</MenuItem>
                        <MenuItem value={"center"}>Center</MenuItem>
                        <MenuItem value={"right"}>Right</MenuItem>
                    </Select>
                    </FormControl> */}
                </div>
                <br></br>
                <Typography variant="h3" gutterBottom style={{color:'Orange',height:"55px",width:"100%",backgroundColor:"black"}}>
                    Overall Data Insights
                </Typography>
                <br></br>
                <div className="geoPlotDiv">
                    <div>
                        <Plot data={geoPlotDataVar.data} layout={geoPlotDataVar.layout}/>
                    </div>
                    <FormControl fullWidth sx={{ m: 1, width:"100%"}}>
                    <InputLabel id="demo-simple-select-label">Type</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={geoplotSelect}
                        label="Polarity"
                        onChange={handleGeoSelect}
                        sx={{ m: 1, backgroundColor:'white'}}
                    >
                        <MenuItem value={"num_results"}>Num Results</MenuItem>
                        <MenuItem value={"reddit_score"}>Reddit Score</MenuItem>
                        <MenuItem value={"score"}>Score</MenuItem>
                        <MenuItem value={"polarity"}>Polarity</MenuItem>
                    </Select>
                    </FormControl>
                </div>
                <br></br>
                <div className='wordcloud_styles'>
                    <img src={polarWordCloudDataLink} alt="wordcloud" />
                    <FormControl fullWidth sx={{ m: 1, width:"100%"}}>
                    <InputLabel id="demo-simple-select-label">Polarity</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={polaritySelect}
                        label="Polarity"
                        onChange={handleChange}
                        sx={{ m: 1, backgroundColor:'white'}}
                    >
                        <MenuItem value={"All"}>All</MenuItem>
                        <MenuItem value={"left"}>Left</MenuItem>
                        <MenuItem value={"center"}>Center</MenuItem>
                        <MenuItem value={"right"}>Right</MenuItem>
                    </Select>
                    </FormControl>
                </div>
                <Line data={timeNoResults} options={timeoptions}></Line>
                <Line data={timePolarityData} options={timeoptions}></Line>
                <Line data={timeChartData} options={timeoptions}></Line>
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