import React, { useState } from 'react'
import '../css/AccountModify.css';

function AccountModify() {

    const [firstName, setFirstName] = useState("")
    const [lastName, setLastName] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [team, setTeam] = useState("")

    const printVal = () => alert('The submitted values are: \n'+firstName+'\n'+lastName+'\n'+email+'\n'+password+'\n'+team);

    return (
        <>
            <div className='offset' >
                <h1> Manage account </h1>
                <h1> Welcome, Firstname Lastname </h1>
                <div className='column'>
                    <h2>Pick team</h2>
                    <h2>Change first name</h2>
                    <h2>Change last name</h2>
                    <h2>Change email</h2>
                    <h2>Change password</h2>
                </div>
                <div className='column'>
                    <form>
                        <select id="teamSelect" onChange={(e) => setTeam(e.target.value)}>
                            <option>Team A</option>
                            <option>Team B</option>
                            <option>Team C</option>
                        </select>
                    </form>
                    <input type="text" placeholder="Current first name" value={firstName} onChange={(e) => setFirstName(e.target.value)}/>
                    <input type="text" placeholder="Current last name" value={lastName} onChange={(e) => setLastName(e.target.value)}/>
                    <br></br>
                    <input type="text" placeholder="Current email" value={email} onChange={(e) => setEmail(e.target.value)}/>
                    <br></br>
                    <input type="text" placeholder="Current password" value={password} onChange={(e) => setPassword(e.target.value)}/>

                    <button onClick={printVal}>Save</button>
                </div>
            </div>
        </>
    )
}

export default AccountModify