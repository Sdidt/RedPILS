import axios from "axios";
import { useState } from "react";

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

const QueryData = async (searchTerm,fromTimeSelect,toTimeSelect,locationName,titleSelect,kValue,allTimeSelect,polaritySelect) => {
    let res
    let toTimeSelectVar
    let fromTimeSelectVar
    console.log(titleSelect)
    const concatenateLocationName = locationName.join(' OR ');
    const whitespaceRemoved = searchTerm.replace(/\s/g, '+')
    toTimeSelectVar = toTimeSelect
    fromTimeSelectVar = fromTimeSelect
    if(allTimeSelect==true){
        toTimeSelectVar = null
        fromTimeSelectVar = null 
    }
    console.log(concatenateLocationName)
    console.log(kValue)
    if(toTimeSelectVar!=null && fromTimeSelectVar!=null && concatenateLocationName!=[]){
        res = await axios.get("http://127.0.0.1:5000/query?query="+whitespaceRemoved+"&from="+fromTimeSelect+"&to="+toTimeSelect+"&region="+concatenateLocationName+"&intitle="+titleSelect+"&k="+kValue+"&polarity="+polaritySelect)
    }
    else if(toTimeSelectVar!=null && fromTimeSelectVar!=null ){
        res = await axios.get("http://127.0.0.1:5000/query?query="+whitespaceRemoved+"&from="+fromTimeSelect+"&to="+toTimeSelect+"&intitle="+titleSelect+"&k="+kValue+"&polarity="+polaritySelect)
    }
    else if(concatenateLocationName!=[]){
        res = await axios.get("http://127.0.0.1:5000/query?query="+whitespaceRemoved+"&region="+concatenateLocationName+"&intitle="+titleSelect+"&k="+kValue+"&polarity="+polaritySelect)
    }
    else{
        res = await axios.get("http://127.0.0.1:5000/query?query="+whitespaceRemoved+"&intitle="+titleSelect+"&k="+kValue+"&polarity="+polaritySelect)
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

const QueryWordcloudData = async(searchTerm,fromTimeSelect,toTimeSelect,locationName,titleSelect,kValue,allTimeSelect,polaritySelect) => {
    let res
    let res_link
    let toTimeSelectVar
    let fromTimeSelectVar
    console.log(titleSelect)
    const concatenateLocationName = locationName.join(' OR ');
    const whitespaceRemoved = searchTerm.replace(/\s/g, '+')
    toTimeSelectVar = toTimeSelect
    fromTimeSelectVar = fromTimeSelect
    if(allTimeSelect==true){
        toTimeSelectVar = null
        fromTimeSelectVar = null 
    }
    console.log(concatenateLocationName)
    console.log(kValue)
    if(toTimeSelectVar!=null && fromTimeSelectVar!=null && concatenateLocationName!=[]){
        res_link = "http://127.0.0.1:5000/api/query_wordcloud?query="+whitespaceRemoved+"&from="+fromTimeSelect+"&to="+toTimeSelect+"&region="+concatenateLocationName+"&intitle="+titleSelect+"&k="+kValue+"&polarity="+polaritySelect
        res = await axios.get("http://127.0.0.1:5000/api/query_wordcloud?query="+whitespaceRemoved+"&from="+fromTimeSelect+"&to="+toTimeSelect+"&region="+concatenateLocationName+"&intitle="+titleSelect+"&k="+kValue+"&polarity="+polaritySelect)
    }
    else if(toTimeSelectVar!=null && fromTimeSelectVar!=null ){
        res_link = "http://127.0.0.1:5000/api/query_wordcloud?query="+whitespaceRemoved+"&from="+fromTimeSelect+"&to="+toTimeSelect+"&intitle="+titleSelect+"&k="+kValue+"&polarity="+polaritySelect
        res = await axios.get("http://127.0.0.1:5000/api/query_wordcloud?query="+whitespaceRemoved+"&from="+fromTimeSelect+"&to="+toTimeSelect+"&intitle="+titleSelect+"&k="+kValue+"&polarity="+polaritySelect)
    }
    else if(concatenateLocationName!=[]){
        res_link = "http://127.0.0.1:5000/api/query_wordcloud?query="+whitespaceRemoved+"&region="+concatenateLocationName+"&intitle="+titleSelect+"&k="+kValue+"&polarity="+polaritySelect
        res = await axios.get("http://127.0.0.1:5000/api/query_wordcloud?query="+whitespaceRemoved+"&region="+concatenateLocationName+"&intitle="+titleSelect+"&k="+kValue+"&polarity="+polaritySelect)
    }
    else{
        res_link = "http://127.0.0.1:5000/api/query_wordcloud?query="+whitespaceRemoved+"&intitle="+titleSelect+"&k="+kValue+"&polarity="+polaritySelect
        res = await axios.get("http://127.0.0.1:5000/api/query_wordcloud?query="+whitespaceRemoved+"&intitle="+titleSelect+"&k="+kValue+"&polarity="+polaritySelect)
    }
    console.log(res)
    if (res == null){
        console.log("oops")
        return;
    }
    else{
        console.log("pass")
    }
    return res_link

}

const QueryGeoPlotData = async(geoPlotKey,colormap) => {
    let res 
    // console.log(colormap)
    res = await axios.get("http://127.0.0.1:5000/api/geoplot?key="+geoPlotKey+"&colormap="+colormap)

    console.log(res)
    if (res == null){
        console.log("oops")
        return;
    }
    else{
        console.log(res.data)
    }
    const res_data = res.data
    return res_data

}

const QueryPolarWordCloud = async(polaritySelect)=>{
    let res
    let res_link

    res_link = "http://127.0.0.1:5000/api/polarity_wordcloud?polarity="+polaritySelect
    res = await axios.get("http://127.0.0.1:5000/api/polarity_wordcloud?polarity="+polaritySelect)
    console.log(res)
    if (res == null){
        console.log("oops")
        return;
    }
    else{
        console.log(res.data)
    }
    return res_link
}

const QueryTimePlot = async()=>{
    let res 
    // console.log(colormap)
    res = await axios.get("http://127.0.0.1:5000/api/timedf")

    console.log(res)
    if (res == null){
        console.log("oops")
        return;
    }
    else{
        console.log(res.data)
    }
    const res_data = res.data
    return res_data

}

const export_const = {
    QueryData,
    QueryStatsData,
    QueryWordcloudData,
    QueryGeoPlotData,
    QueryPolarWordCloud,
    QueryTimePlot,
}

export default export_const;
