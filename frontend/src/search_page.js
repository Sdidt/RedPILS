import React, { useEffect, useState } from 'react';
import Iframe from 'react-iframe-click';
import { ReactSearchAutocomplete } from 'react-search-autocomplete'
import Dropdown from 'react-dropdown';
import Multiselect from 'multiselect-react-dropdown';
import 'react-dropdown/style.css';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import Autocomplete from '@mui/material/Autocomplete';
import DATA from './services/datalist'
import SearchResultsComp from './search_results_comp';
import InsightsComp from './insights_comp';
import NoResultsImg from "./pic1.png";

const SearchPage = () => {

  const [dataCollect, setDataCollect] = useState([]);
  const [filterDataCollect, setFilterDataCollect] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [timeSelectConst, setTimeSelectConst] = useState("All")
  const [statsCheck , setStatsCheck] = useState(0)
  const [alignment, setAlignment] = React.useState('searchResults');
  const [redditScoreAll, setRedditScoreAll] = React.useState('all');

  // const [categories,setCategories] = useState([])
  // const [dataCounts,setDataCounts] = useState([])


  const handleSearch=(e)=>{
      e.preventDefault();
  }
  const items = [
      {
        id: 0,
        name: 'BJP'
      },
      {
        id: 1,
        name: 'Congress'
      },
      {
        id: 2,
        name: 'AAP'
      },
      {
        id: 3,
        name: 'Kejriwal'
      },
      {
        id: 4,
        name: 'Bla'
      }
    ]

  const timeDropDown = [
    'All', '1M', '3M','12M','24M'
  ];
  const timeDropDownDefault = timeDropDown[0];

  const redditPolarityDropDown = [
    'All', '+ve', '-ve'
  ];
  const redditPolarityDefault = redditPolarityDropDown[0];

  const multiselectoptions = {
    options: [{name: 'Option 1️⃣', id: 1},{name: 'Option 2️⃣', id: 2}]
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

  const [barChartData, setBarChartData] = useState(data);
  const [pieChartData, setPieChartData] = useState(data);
  const [doughChartData, setDoughChartData] = useState(data);
  
  const handleOnSearch = async(string, results) => {
    if(string!=''){
      setSearchTerm(string)
    }
  }

  const handleOnHover = (result) => {
    // the item hovered
    // console.log(result)
  }

  const handleOnSelect = (item) => {
    // the item selected
    // console.log(item)
  }

  const handleOnFocus = () => {
    // console.log('Focused')
  }

  const handleButtonSearch = async(searchTerm,timeSelectConst) => {
    console.log(searchTerm)
    console.log(timeSelectConst)
    if(searchTerm!=""){
      var dummy_data_store = await DATA.QueryData(searchTerm,timeSelectConst)
      console.log(dummy_data_store['topk'])
      setDataCollect(dummy_data_store['topk'])
      setFilterDataCollect(dummy_data_store['topk'])

      var dummy_data_store = await DATA.QueryStatsData()
      setStatsCheck(dummy_data_store['x-val-num-fieldname'].length)
      var dataCounts = dummy_data_store['x-val-num-fieldname']
      var categories = dummy_data_store['x-val-cat-fieldname']
      console.log(dummy_data_store)
      // setDataCounts(dummy_data_store['x-val-num-fieldname'])
      // setCategories(dummy_data_store['x-val-cat-fieldname'])
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
    }
  }

  console.log(barChartData)

  const handleKeywordSearch = async(searchTerm) => {
    const dummy_data_store = await DATA.QueryData(searchTerm,timeSelectConst)
    if(dummy_data_store['topk'].length==0){
      const dummy_data_store = await DATA.QueryData('BJP')
    }
    setDataCollect(dummy_data_store['topk'])
    setFilterDataCollect(dummy_data_store['topk'])
  }

  const formatResult = (item) => {
    return (
      <>
        {/* <span style={{ display: 'block', textAlign: 'left' }}>id: {item.id}</span>
        <span style={{ display: 'block', textAlign: 'left' }}>name: {item.name}</span> */}
        <span style={{ display: 'block', textAlign: 'left' }}>{item.name}</span>
      </>
    )
  }

  const handleRedditScoreSelect = (selectItem) => {
    if(selectItem.value == "+ve"){
      const dataCollectFilter =  dataCollect.filter(function(dataObj) {
        return dataObj.reddit_score >= 0;
      });
      setFilterDataCollect(dataCollectFilter)
    }
    else if(selectItem.value == "-ve"){
      const dataCollectFilter =  dataCollect.filter(function(dataObj) {
        return dataObj.reddit_score < 0;
      });
      setFilterDataCollect(dataCollectFilter)
    }
    else{
      setFilterDataCollect(dataCollect)
    }
  }

  const handleDateSelect = (selectItem) => {
    if(selectItem.value != "All"){
    var timeDummy = (selectItem.value).substring(0,((selectItem.value).length-1))
    setTimeSelectConst(timeDummy)}
    else{
      setTimeSelectConst("All")
    }
  }

  const handleToggleChange = (element) => {
    setAlignment(element.target.value)
  }

  const handleScoreChange = (element) => {
    setRedditScoreAll(element.target.value)
    if(element.target.value == "positiveScore"){
      const dataCollectFilter =  dataCollect.filter(function(dataObj) {
        return dataObj.reddit_score >= 0;
      });
      setFilterDataCollect(dataCollectFilter)
    }
    else if(element.target.value == "negativeScore"){
      const dataCollectFilter =  dataCollect.filter(function(dataObj) {
        return dataObj.reddit_score < 0;
      });
      setFilterDataCollect(dataCollectFilter)
    }
    else{
      setFilterDataCollect(dataCollect)
    }
  }

  useEffect (() => {
    console.log("inside use effect")
    const getData = async () => {
      const dummy_data_store = await DATA.QueryData('BJP')
      console.log(dummy_data_store['topk'])
      setDataCollect(dummy_data_store['topk'])
    }
  },[dataCollect,filterDataCollect])

  return (
    <div className='SearchPageMain'>
    <div className='SearchPageResults'>
        <div className='SearchResults1'>
          <div className='SearchBarDiv'>
            <div className='SearchBar'>
              <ReactSearchAutocomplete
                  items={items}
                  onSearch={handleOnSearch}
                  onHover={handleOnHover}
                  onSelect={handleOnSelect}
                  onFocus={handleOnFocus}
                  autoFocus
                  showIcon={true}
                  placeholder="Search"
                  formatResult={formatResult}
                  styling={{borderRadius: "8px",zIndex:999}}
              />
            </div>
            {/* <div class="vl"></div> */}
            <div className='searchFiltersDiv'>
              <div className='dropdowndiv'>
                <Dropdown onChange={handleDateSelect}  options={timeDropDown} value={timeDropDownDefault} placeholder="Select an option" className='dropdownindv' />
              </div>
              <br/>
              <div className='dropdowndiv'>
                <Multiselect
                options={multiselectoptions.options} // Options to display in the dropdown
                // selectedValues={this.state.selectedValue} // Preselected value to persist in dropdown
                // onSelect={this.onSelect} // Function will trigger on select event
                // onRemove={this.onRemove} // Function will trigger on remove event
                displayValue="name" // Property name to display in the dropdown options
                />
              </div>
            </div>
            <button className='SearchButton' onClick={()=>handleButtonSearch(searchTerm,timeSelectConst)}>Search</button>
          </div>
          <div className='filtersDiv'>
            <div className='toggleTabDiv'>
              <ToggleButtonGroup
                color="primary"
                value={alignment}
                exclusive
                onChange={handleToggleChange}
                aria-label="Platform"
              >
                <ToggleButton value="redditScore" style={{color:"#ff4500" , backgroundColor:"#161515"}}>Type : </ToggleButton>
                <ToggleButton value="searchResults" style={{color: 'white'}}>Search Results</ToggleButton>
                <ToggleButton value="insights" style={{color: 'white'}}>Insights</ToggleButton>
              </ToggleButtonGroup>
            </div>
            <div className='ToggleScoreDiv'>
              <ToggleButtonGroup
                color="primary"
                value={redditScoreAll}
                exclusive
                onChange={handleScoreChange}
                aria-label="Platform"
              >
                <ToggleButton value="redditScore" style={{color:"#ff4500" , backgroundColor:"#161515"}}>Reddit Score :</ToggleButton>
                <ToggleButton value="all" style={{color: 'white'}}>All</ToggleButton>
                <ToggleButton value="positiveScore" style={{color: 'white'}}>+ve</ToggleButton>
                <ToggleButton value="negativeScore" style={{color: 'white'}}>-ve</ToggleButton>
              </ToggleButtonGroup>
            </div>
          </div>
          <br/>
          {alignment == 'searchResults' ? (
            <SearchResultsComp 
            data = {filterDataCollect}/>
            ):(
            <InsightsComp
            barChartData = {barChartData}
            pieChartData = {pieChartData} 
            doughChartData = {doughChartData}
            statsCheck = {statsCheck}/>
            )
          }
        </div>
        <div className="side-box">
            <div>
                Top searched terms
            </div>
            <br/>
            <div className='buttons-start'>
            {items.map((object_ele,i)=>
            <button className='btn-orange' onClick={()=>handleKeywordSearch(object_ele.name)} key={i}>{object_ele.name}</button>
            )}
            </div>
        </div>
    </div>
    </div>
  );
}

export default SearchPage;
