import React from 'react';
import ReactWordcloud from 'react-wordcloud';
 
const SimpleWordcloud = () => {
    const words = [
        {
            text: 'Extremely valid points but I believe he has the charisma to win over urban youth who is usually the most apathetic (non) voter. Although, I would keep my expectations low since Tharoor has a ton of intra-party politics to deal with.',
            value: 64,
        },
        {
            text: "If they focused on campaigning in urban areas with development issue, I think they can win anywhere in India. It's just the rural areas that become a little tricky to tackle.",
            value: 11,
        },
        {
            text: "What else can you expect from Godi Media. All they talk about is Pakistan, Mudi, Yogi, ramdev, some random ass babas and group discussions on who will win the next cricket match...",
            value: 16,
        },
        {
            text: "But is Art. 14 also supposed to determine the policies of the government in the matters of citizenship or deportation? Personally, I would have preferred no exclusion of any persecuted minorities irrespective of their religion or lack of, orientation, race etc. But, since this is a policy matter, I don't see it as an infringement to our constitutional rights. No, ofcourse not. How can anyone support such a barbaric and oppressive framework. I will actively join any protests that would get formed then. But, I do believe in our constitution and our judiciary. They are there to stop such a thing from ever happening. But at the moment, logically, I can't support or adhere to any protest on the foundation of a hypothesis or an assumption. That's not how any democracy works.",
            value: 17,
        },
        ]
    
    const callbacks = {
        getWordColor: word => word.value > 50 ? "blue" : "red",
        onWordClick: console.log,
        onWordMouseOver: console.log,
        getWordTooltip: word => `${word.text} (${word.value}) [${word.value > 50 ? "good" : "bad"}]`,
        }
    return (
        <ReactWordcloud callbacks={callbacks} words={words} />
    )
}

export default SimpleWordcloud