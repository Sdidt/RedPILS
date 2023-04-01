import axios from "axios";

const DummyQueryData = async () => {
    const res = await axios.get("http://127.0.0.1:5000/dummy_query")
    if (res == null){
        console.log("oops")
        return;
    }
    else{
        console.log(res.data)
    }
    const res_data = res.data
    return res_data;
};

const QueryStatsData = async () => {
    const res = await axios.get("http://127.0.0.1:5000//dummy_charts2d")
    console.log(res)
    if (res == null){
        console.log("oops")
        return;
    }
    else{
        console.log(res.data)
    }
    const res_data = res.data
    return res_data;
}

const QueryData = async (searchTerm,fromTimeSelect,toTimeSelect,locationName,titleSelect,kValue) => {
    let res
    const concatenateLocationName = locationName.join(' OR ');
    const whitespaceRemoved = searchTerm.replace(/\s/g, '+')
    console.log(concatenateLocationName)
    console.log(kValue)
    if(toTimeSelect!=null && fromTimeSelect!=null && concatenateLocationName!=[]){
        res = await axios.get("http://127.0.0.1:5000/query?query="+whitespaceRemoved+"&from="+fromTimeSelect+"&to="+toTimeSelect+"&region="+concatenateLocationName+"&intitle="+titleSelect+"&k="+kValue)
    }
    else if(toTimeSelect!=null && fromTimeSelect!=null ){
        res = await axios.get("http://127.0.0.1:5000/query?query="+whitespaceRemoved+"&from="+fromTimeSelect+"&to="+toTimeSelect+"&intitle="+titleSelect+"&k="+kValue)
    }
    else if(concatenateLocationName!=[]){
        console.log("hello")
        res = await axios.get("http://127.0.0.1:5000/query?query="+whitespaceRemoved+"&region="+concatenateLocationName+"&intitle="+titleSelect+"&k="+kValue)
    }
    else{
        console.log("hello")
        res = await axios.get("http://127.0.0.1:5000/query?query="+whitespaceRemoved+"&intitle="+titleSelect+"&k="+kValue)
    }
    console.log(res)
    if (res == null){
        console.log("oops")
        return;
    }
    else{
        console.log(res.data)
    }
    const res_data = res.data
    return res_data;
}

const export_const = {
    QueryData,
    QueryStatsData
}

export default export_const;
