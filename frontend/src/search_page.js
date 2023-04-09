import React, { useEffect, useState } from "react";
import Iframe from "react-iframe-click";

// Autocomplete
import { ReactSearchAutocomplete } from "react-search-autocomplete";
import Dropdown from "react-dropdown";
// import Multiselect from 'multiselect-react-dropdown';
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";

// Toggle button imports
import "react-dropdown/style.css";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import Box from "@mui/material/Box";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";

// Accordian Imports
import { ArrowForwardSharp } from "@mui/icons-material";
import MuiAccordion, { AccordionProps } from "@mui/material/Accordion";
import MuiAccordionSummary, {
  AccordionSummaryProps,
} from "@mui/material/AccordionSummary";
import MuiAccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import { styled } from "@mui/material/styles";

// Multi select component
import OutlinedInput from "@mui/material/OutlinedInput";
import ListItemText from "@mui/material/ListItemText";
import Checkbox from "@mui/material/Checkbox";

// Date Component
import { DemoContainer } from "@mui/x-date-pickers/internals/demo";
import { LocalizationProvider } from "@mui/x-date-pickers-pro";
import { AdapterDayjs } from "@mui/x-date-pickers-pro/AdapterDayjs";
import { DateRangePicker } from "@mui/x-date-pickers-pro/DateRangePicker";
import dayjs from "dayjs";

// Data and Component imports
import DATA from "./services/datalist";
import SearchResultsComp from "./search_results_comp";
import InsightsComp from "./insights_comp";
import NoResultsImg from "./pic1.png";

// Checkbox
import FormGroup from "@mui/material/FormGroup";
import FormControlLabel from "@mui/material/FormControlLabel";

const SearchPage = () => {
  const [dataCollect, setDataCollect] = useState([]);
  const [filterDataCollect, setFilterDataCollect] = useState([]);
  const [wordCloudData, setWordCloudData] = useState([]);
  const [polarWordCloudData, setPolarWordCloudData] = useState([]);
  const [geoPlotData, setGeoPlotData] = useState([]);
  const [timePlotData, setTimePlotData] = useState([]);
  const [timePolarityData, setTimePolarityData] = useState([]);
  const [timeNoResults, setTimeNoResults] = useState([]);
  const [numResults, setNumResults] = useState("");
  const [avgRedditScore, setAvgRedditScore] = useState("");
  const [avgScore, setAvgScore] = useState("");
  const [searchTime, setSearchTime] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [timeSelect, setTimeSelect] = useState([null, null]);
  const [fromTimeSelect, setFromTimeSelect] = useState(null);
  const [toTimeSelect, setToTimeSelect] = useState(null);
  const [timeSelectConst, setTimeSelectConst] = useState("All");
  const [statsCheck, setStatsCheck] = useState(0);
  const [alignment, setAlignment] = React.useState("searchResults");
  const [redditScoreAll, setRedditScoreAll] = React.useState("all");
  const [locationName, setLocationName] = useState([]);
  const [timeframe, setTimeFrame] = useState("All");
  const [kValue, setKValue] = useState("10");
  const [titleValue, setTitleValue] = React.useState("");
  const [titleSelect, setTitleSelect] = useState(false);
  const [allTimeSelect, setAllTimeSelect] = useState(true);
  const [polaritySelect, setPolaritySelect] = useState('All')
  const [expanded, setExpanded] = useState(false);

  // const [categories,setCategories] = useState([])
  // const [dataCounts,setDataCounts] = useState([])

  const handleSearch = (e) => {
    e.preventDefault();
  };
  const items = [
    {
      id: 0,
      name: "BJP",
    },
    {
      id: 1,
      name: "Congress",
    },
    {
      id: 2,
      name: "AAP",
    },
    {
      id: 3,
      name: "Kejriwal",
    },
    {
      id: 4,
      name: "Tharoor",
    },
    {
      id: 5,
      name: "Punjab",
    },
    {
      id: 6,
      name: "Government",
    },
    {
      id: 7,
      name: "Education",
    },
    {
      id: 8,
      name: "Modi",
    },
  ];

  const top100Films = [
    { label: "The Shawshank Redemption", year: 1994 },
    { label: "The Godfather", year: 1972 },
    { label: "The Godfather: Part II", year: 1974 },
    { label: "The Dark Knight", year: 2008 },
    { label: "12 Angry Men", year: 1957 },
    { label: "Schindler's List", year: 1993 },
    { label: "Pulp Fiction", year: 1994 },
    {
      label: "The Lord of the Rings: The Return of the King",
      year: 2003,
    },
  ];

  const ITEM_HEIGHT = 48;
  const ITEM_PADDING_TOP = 8;
  const MenuProps = {
    PaperProps: {
      style: {
        maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
        width: 250,
      },
    },
  };

  const LocationNames = [
    "Andaman and Nicobar",
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chandigarh",
    "Chhattisgarh",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jammu and Kashmir",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Ladakh",
    "Lakshadweep",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Puducherry",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Union territory",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "India",
    "China",
    "Pakistan",
    "Sri Lanka",
    "Britain",
    "Bangladesh",
    "Afghanistan",
  ];

  const timeDropDown = ["All", "1M", "3M", "12M", "24M"];
  const timeDropDownDefault = timeDropDown[0];

  const redditPolarityDropDown = ["All", "+ve", "-ve"];
  const redditPolarityDefault = redditPolarityDropDown[0];

  const multiselectoptions = {
    options: [
      { name: "Option 1️⃣", id: 1 },
      { name: "Option 2️⃣", id: 2 },
    ],
  };

  const redditdata = {
    labels: [],
    datasets: [
      {
        label: "Avg Reddit Score",
        data: [],
        backgroundColor: [
          "#3e95cd",
          "#8e5ea2",
          "#3cba9f",
          "#e8c3b9",
          "#c45850",
        ],
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
      },
    ],
  };

  const countdata = {
    labels: [],
    datasets: [
      {
        label: "Counts",
        data: [],
        backgroundColor: [
          "#3e95cd",
          "#8e5ea2",
          "#3cba9f",
          "#e8c3b9",
          "#c45850",
        ],
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
      },
    ],
  };

  const timedata = {
    labels: [],
    datasets: [
      {
        label: 'Dataset 1',
        data: [],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
    ],
  };

  const [barChartDataCount, setBarChartDataCount] = useState(countdata);
  const [barChartDataScore, setBarChartDataScore] = useState(redditdata);
  const [timeChartData, setTimeChartData] = useState(timedata);
  const [pieChartData, setPieChartData] = useState(redditdata);
  const [doughChartData, setDoughChartData] = useState(redditdata);

  const handleOnSearch = async (string, results) => {
    if (string != "") {
      setSearchTerm(string);
    }
  };

  const handleOnHover = (result) => {
    // the item hovered
    // console.log(result)
  };

  const handleOnSelect = (item) => {
    // the item selected
    if (item.name != "") {
      setSearchTerm(item.name);
    }
    console.log(item.name);
  };

  const handleOnFocus = () => {
    // console.log('Focused')
  };

  const handleButtonSearch = async (
    searchTerm,
    fromTimeSelect,
    toTimeSelect,
    locationName,
    titleSelect,
    kValue,
    allTimeSelect,
    polaritySelect
  ) => {
    console.log(searchTerm);
    console.log(timeSelectConst);
    console.log(locationName);
    console.log(kValue);
    if (searchTerm != "") {
      var dummy_data_store = await DATA.QueryData(
        searchTerm,
        fromTimeSelect,
        toTimeSelect,
        locationName,
        titleSelect,
        kValue,
        allTimeSelect,
        polaritySelect
      );
      var dummy_wordcloud_data = await DATA.QueryWordcloudData(
        searchTerm,
        fromTimeSelect,
        toTimeSelect,
        locationName,
        titleSelect,
        kValue,
        allTimeSelect,
        polaritySelect
      );
      var dummy_geoplot_data = await DATA.QueryGeoPlotData(
        "num_results",
        "Blues"
      );
      var dummy_polar_wordcloud = await DATA.QueryPolarWordCloud(
        polaritySelect
      );
      var dummy_time_data = await DATA.QueryTimePlot()
      console.log(dummy_time_data)
      setGeoPlotData(dummy_geoplot_data);
      setWordCloudData(dummy_wordcloud_data);
      setPolarWordCloudData(dummy_polar_wordcloud);
      setDataCollect(dummy_data_store["topk"]);
      setFilterDataCollect(dummy_data_store["topk"]);
      setNumResults(dummy_data_store["num_results"]);
      setAvgRedditScore(dummy_data_store["avg_reddit_score"]);
      setAvgScore(dummy_data_store["avg_score"]);
      setSearchTime(dummy_data_store["search_time"]);
      var dataCounts = dummy_data_store["query_polarity_counts"];
      var dataPolarScores = dummy_data_store["polarity_reddit_scores"];
      var categories = dummy_data_store["x_label"];
      var timePolarScores = dummy_time_data['polarity']
      var timeRedditScore = dummy_time_data['reddit_score']
      var timenoresults = dummy_time_data['num_results']
      var timeCategories = dummy_time_data['month']

      var dummy_data_store = await DATA.QueryStatsData();
      setStatsCheck(dummy_data_store["x-val-num-fieldname"].length);
      // var dataCounts = dummy_data_store["x-val-num-fieldname"];
      // var categories = dummy_data_store["x-val-cat-fieldname"];
      console.log(dummy_data_store);
      setBarChartDataScore({
        ...redditdata,
        labels: categories,
        datasets: [
          {
            ...redditdata.datasets[0],
            data: dataPolarScores,
          },
        ],
      });
      setBarChartDataCount({
        ...countdata,
        labels: categories,
        datasets: [
          {
            ...countdata.datasets[0],
            data: dataCounts,
          },
        ],
      });

      setPieChartData({
        ...redditdata,
        labels: categories,
        datasets: [
          {
            ...redditdata.datasets[0],
            data: dataCounts,
          },
        ],
      });

      setDoughChartData({
        ...redditdata,
        labels: categories,
        datasets: [
          {
            ...redditdata.datasets[0],
            data: dataCounts,
          },
        ],
      });

      setTimeChartData({
        ...timedata,
        labels: timeCategories,
        datasets:[
          {
            ...timedata.datasets[0],
            data:timeRedditScore,
            label:"Avg Reddit Score Over time",
          }
        ]
      });
      setTimeNoResults({
        ...timedata,
        labels: timeCategories,
        datasets:[
          {
            ...timedata.datasets[0],
            data:timenoresults,
            label:"No of Results Over time",
          }
        ]
      });
      setTimePolarityData({
        ...timedata,
        labels: timeCategories,
        datasets:[
          {
            ...timedata.datasets[0],
            data:timePolarScores,
            label:"Average Polarity Over time",
          }
        ]
      });
    }
  };
  const handleKeywordSearch = async (searchTerm) => {
    const dummy_data_store = await DATA.QueryData(
      searchTerm,
      fromTimeSelect,
      toTimeSelect,
      locationName,
      titleSelect,
      kValue,
      allTimeSelect,
      polaritySelect
    );
    var dummy_wordcloud_data = await DATA.QueryWordcloudData(
      searchTerm,
      fromTimeSelect,
      toTimeSelect,
      locationName,
      titleSelect,
      kValue,
      allTimeSelect,
      polaritySelect
    );
    var dummy_geoplot_data = await DATA.QueryGeoPlotData("num_results",'Blues');
    var dummy_polar_wordcloud = await DATA.QueryPolarWordCloud(
      polaritySelect
    )
    setGeoPlotData(dummy_geoplot_data);
    setWordCloudData(dummy_wordcloud_data);
    if (dummy_data_store["topk"].length == 0) {
      const dummy_data_store = await DATA.QueryData("BJP");
    }
    setPolarWordCloudData(dummy_polar_wordcloud);
    setDataCollect(dummy_data_store["topk"]);
    setFilterDataCollect(dummy_data_store["topk"]);
  };

  const formatResult = (item) => {
    return (
      <>
        {/* <span style={{ display: 'block', textAlign: 'left' }}>id: {item.id}</span>
        <span style={{ display: 'block', textAlign: 'left' }}>name: {item.name}</span> */}
        <span style={{ display: "block", textAlign: "left" }}>{item.name}</span>
      </>
    );
  };

  const handleRedditScoreSelect = (selectItem) => {
    if (selectItem.value == "+ve") {
      const dataCollectFilter = dataCollect.filter(function (dataObj) {
        return dataObj.reddit_score >= 0;
      });
      setFilterDataCollect(dataCollectFilter);
    } else if (selectItem.value == "-ve") {
      const dataCollectFilter = dataCollect.filter(function (dataObj) {
        return dataObj.reddit_score < 0;
      });
      setFilterDataCollect(dataCollectFilter);
    } else {
      setFilterDataCollect(dataCollect);
    }
  };

  const handleDateSelect = (selectItem) => {
    if (selectItem.value != "All") {
      var timeDummy = selectItem.value.substring(
        0,
        selectItem.value.length - 1
      );
      setTimeSelectConst(timeDummy);
    } else {
      setTimeSelectConst("All");
    }
  };

  const handleToggleChange = (element) => {
    setAlignment(element.target.value);
  };

  const handleScoreChange = (element) => {
    setRedditScoreAll(element.target.value);
    if (element.target.value == "positiveScore") {
      const dataCollectFilter = dataCollect.filter(function (dataObj) {
        return dataObj.reddit_score >= 0;
      });
      setFilterDataCollect(dataCollectFilter);
    } else if (element.target.value == "negativeScore") {
      const dataCollectFilter = dataCollect.filter(function (dataObj) {
        return dataObj.reddit_score < 0;
      });
      setFilterDataCollect(dataCollectFilter);
    } else {
      setFilterDataCollect(dataCollect);
    }
  };

  const handleLocationChange = (
    event: SelectChangeEvent<typeof personName>
  ) => {
    const {
      target: { value },
    } = event;
    setLocationName(
      // On autofill we get a stringified value.
      typeof value === "string" ? value.split(",") : value
    );
  };

  const handleTimeFrameSelect = (event: SelectChangeEvent) => {
    setTimeFrame(event.target.value);
  };

  // const handleKSelect = (event) => {
  //   console.log(event.target.value)
  //   setKValue(event.target.value)
  // }

  const handleTitleChange = (event) => {
    console.log(event.target.value);
    setTitleValue(event.target.value);
  };

  const handleDateChange = (newValue) => {
    if (newValue[0] && newValue[1]) {
      const startFormatted = dayjs(newValue[0]).format("DDMMYYYY");
      const endFormatted = dayjs(newValue[1]).format("DDMMYYYY");
      setFromTimeSelect(startFormatted);
      setToTimeSelect(endFormatted);
      setTimeSelect(newValue);
    }
  };

  const handleTitleSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    setTitleSelect(event.target.checked);
  };

  const handleAllTimeSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAllTimeSelect(event.target.checked);
  };

  const handlePolaritySelect = (event: SelectChangeEvent) => {
    setPolaritySelect(event.target.value)
}

  const Accordion = styled((props: AccordionProps) => (
    <MuiAccordion disableGutters elevation={0} square {...props} />
  ))(({ theme }) => ({
    border: `2px solid ${theme.palette.divider}`,
    borderRadius: "8px",
    backgroundColor: "rgb(220, 220, 220)",
    // color: 'rgb(255, 69, 0)',
    color: "black",
    "&:not(:last-child)": {
      borderBottom: 0,
    },
    "&:before": {
      display: "none",
    },
  }));

  const AccordionSummary = styled((props: AccordionSummaryProps) => (
    <MuiAccordionSummary
      expandIcon={<ArrowForwardSharp sx={{ fontSize: "0.9rem" }} />}
      {...props}
    />
  ))(({ theme }) => ({
    backgroundColor:
      theme.palette.mode === "dark"
        ? "rgba(255, 255, 255, .05)"
        : "rgba(0, 0, 0, .03)",
    flexDirection: "row-reverse",
    "& .MuiAccordionSummary-expandIconWrapper.Mui-expanded": {
      transform: "rotate(90deg)",
    },
    "& .MuiAccordionSummary-content": {
      marginLeft: theme.spacing(1),
    },
  }));

  const AccordionDetails = styled(MuiAccordionDetails)(({ theme }) => ({
    padding: theme.spacing(2),
    borderTop: "1px solid rgba(0, 0, 0, .125)",
  }));

  useEffect(() => {
    console.log("inside use effect");
  }, [dataCollect, filterDataCollect, geoPlotData, wordCloudData]);

  return (
    <div className="SearchPageMain">
      <div className="SearchPageResults">
        <div className="SearchResults1">
          <div className="SearchBarDiv">
            <div className="SearchBar">
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
                styling={{ borderRadius: "8px", zIndex: 999 }}
              />
              <br />
              <Accordion
                expanded={expanded}
                onChange={() => setExpanded(!expanded)}
                style={{ alignItems: "center", justifyContent: "center" }}
              >
                <AccordionSummary
                  aria-controls="panel1d-content"
                  id="panel1d-header"
                >
                  <Typography>Advanced Search</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <div className="searchFiltersDiv">
                    {/* <TextField 
                  id="outlined-basic" 
                  label="Title Search" 
                  variant="outlined" 
                  defaultValue={titleValue}
                  sx={{ m: 1, backgroundColor:'white', width:"30%"}} 
                  onBlur={(event: React.ChangeEvent<HTMLInputElement>) => {
                    setTitleValue(event.target.value);
                  }}/> */}
                    <FormGroup
                      sx={{
                        m: 1,
                        width: "15%",
                        backgroundColor: "white",
                        border: "1px solid rgb(184, 184, 184)",
                        borderRadius: "2px",
                        paddingLeft: "1%",
                      }}
                    >
                      <FormControlLabel
                        control={<Checkbox defaultChecked />}
                        label="Intitle Search"
                        checked={titleSelect}
                        onChange={handleTitleSelect}
                      />
                    </FormGroup>
                    <FormControl
                      sx={{ m: 1, width: "40%", backgroundColor: "white" }}
                      expanded={expanded}
                    >
                      <InputLabel id="demo-multiple-checkbox-label">
                        Location
                      </InputLabel>
                      <Select
                        labelId="demo-multiple-checkbox-label"
                        id="demo-multiple-checkbox"
                        multiple
                        value={locationName}
                        onChange={handleLocationChange}
                        onSelect={() => setExpanded(!expanded)}
                        input={<OutlinedInput label="Tag" />}
                        renderValue={(selected) => selected.join(", ")}
                        MenuProps={MenuProps}
                      >
                        {LocationNames.map((name) => (
                          <MenuItem key={name} value={name}>
                            <Checkbox
                              checked={locationName.indexOf(name) > -1}
                            />
                            <ListItemText primary={name} />
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                    {/* <FormControl sx={{ m: 1, width: "15%", backgroundColor:'white'}}>
                    <InputLabel id="demo-simple-select-label">TimeFrame</InputLabel>
                    <Select
                      labelId="demo-simple-select-label"
                      id="demo-simple-select"
                      value={timeframe}
                      label="Age"
                      onChange={handleTimeFrameSelect}
                    >
                      <MenuItem value={"All"}>All</MenuItem>
                      <MenuItem value={"1"}>1 Month</MenuItem>
                      <MenuItem value={"6"}>6 Months</MenuItem>
                      <MenuItem value={"12"}>12 Months</MenuItem>
                      <MenuItem value={"24"}>24 Months</MenuItem>
                    </Select>
                  </FormControl> */}
                    <TextField
                      id="outlined-basic"
                      label="No of Results"
                      variant="outlined"
                      defaultValue={kValue}
                      sx={{ m: 1, backgroundColor: "white", width: "15%" }}
                      onBlur={(event: React.ChangeEvent<HTMLInputElement>) => {
                        setKValue(event.target.value);
                      }}
                    />
                    <FormControl fullWidth sx={{ m: 1, width:"15%"}}>
                    <InputLabel id="demo-simple-select-label">Polarity</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={polaritySelect}
                        label="Polarity"
                        onChange={handlePolaritySelect}
                        sx={{ m: 1, backgroundColor:'white'}}
                    >
                        <MenuItem value={"All"}>All</MenuItem>
                        <MenuItem value={"left"}>Left</MenuItem>
                        <MenuItem value={"center"}>Center</MenuItem>
                        <MenuItem value={"right"}>Right</MenuItem>
                    </Select>
                    </FormControl>
                  </div>
                  <div className="datePickerDiv">
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                      <DemoContainer components={["DateRangePicker"]}>
                        <DateRangePicker
                          localeText={{ start: "Start", end: "End" }}
                          value={timeSelect}
                          onChange={handleDateChange}
                          sx={{ m: 1, paddingBottom: "1.5%" }}
                        />
                      </DemoContainer>
                    </LocalizationProvider>
                    <FormGroup
                      sx={{
                        width: "15%",
                        backgroundColor: "white",
                        border: "1px solid rgb(184, 184, 184)",
                        borderRadius: "2px",
                        paddingLeft: "1%",
                      }}
                    >
                      <FormControlLabel
                        control={<Checkbox defaultChecked />}
                        label="All time"
                        checked={allTimeSelect}
                        onChange={handleAllTimeSelect}
                      />
                    </FormGroup>
                  </div>
                </AccordionDetails>
              </Accordion>
            </div>
            <button
              className="SearchButton"
              onClick={() =>
                handleButtonSearch(
                  searchTerm,
                  fromTimeSelect,
                  toTimeSelect,
                  locationName,
                  titleSelect,
                  kValue,
                  allTimeSelect,
                  polaritySelect
                )
              }
            >
              Search
            </button>
          </div>
          <div className="filtersDiv">
            <div className="toggleTabDiv">
              <ToggleButtonGroup
                color="primary"
                value={alignment}
                exclusive
                onChange={handleToggleChange}
                aria-label="Platform"
              >
                <ToggleButton
                  value="redditScore"
                  style={{ color: "#ff4500", backgroundColor: "#161515" }}
                >
                  Type :{" "}
                </ToggleButton>
                <ToggleButton value="searchResults" style={{ color: "white" }}>
                  Search Results
                </ToggleButton>
                <ToggleButton value="insights" style={{ color: "white" }}>
                  Insights
                </ToggleButton>
              </ToggleButtonGroup>
            </div>
            <div className="ToggleScoreDiv">
              <ToggleButtonGroup
                color="primary"
                value={redditScoreAll}
                exclusive
                onChange={handleScoreChange}
                aria-label="Platform"
              >
                <ToggleButton
                  value="redditScore"
                  style={{ color: "#ff4500", backgroundColor: "#161515" }}
                >
                  Reddit Score :
                </ToggleButton>
                <ToggleButton value="all" style={{ color: "white" }}>
                  All
                </ToggleButton>
                <ToggleButton value="positiveScore" style={{ color: "white" }}>
                  +ve
                </ToggleButton>
                <ToggleButton value="negativeScore" style={{ color: "white" }}>
                  -ve
                </ToggleButton>
              </ToggleButtonGroup>
            </div>
          </div>
          <br />
          {alignment == "searchResults" ? (
            <SearchResultsComp
              data={filterDataCollect}
              numResults={numResults}
            />
          ) : (
            <InsightsComp
              wordCloudData={wordCloudData}
              barChartDataCount={barChartDataCount}
              barChartDataScore={barChartDataScore}
              pieChartData={pieChartData}
              doughChartData={doughChartData}
              timeChartData={timeChartData}
              timeNoResults={timeNoResults}
              timePolarityData={timePolarityData}
              statsCheck={statsCheck}
              avgRedditScore={avgRedditScore}
              avgScore={avgScore}
              searchTime={searchTime}
              geoPlotData={geoPlotData}
              polarWordCloudData = {polarWordCloudData}
            />
          )}
        </div>
        <div className="side-box">
          <div>Top searched terms</div>
          <br />
          <div className="buttons-start">
            {items.map((object_ele, i) => (
              <button
                className="btn-orange"
                onClick={() => handleKeywordSearch(object_ele.name)}
                key={i}
              >
                {object_ele.name}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchPage;
