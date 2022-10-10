import React, { useState } from 'react'
import { Link } from 'react-router-dom';
import * as FaIcons from 'react-icons/fa';
import * as AiIcons from 'react-icons/ai';
import '../css/Navbar.css';
import { IconContext } from 'react-icons';

function Navbar() {
    return (
        <>
            <IconContext.Provider value={{ color: '#000' }}>
                <nav className='nav-menu'>
                    <ul className='nav-menu-items'>

                        {/* <h1 className='fname'>Farm Name</h1> */}

                        <li className='nav-text'>
                            <Link to='/dashboard'>
                                <AiIcons.AiOutlineHome />
                                <span>Dashboard</span>
                            </Link>
                        </li>

                        <li className='nav-text'>
                            <Link to='/dashboard'>
                                <AiIcons.AiOutlineContainer />
                                <span>Orders</span>
                            </Link>
                        </li>

                        <li className='nav-text'>
                            <Link to='/dashboard'>
                                <AiIcons.AiOutlineDropbox />
                                <span>Packaging</span>
                            </Link>
                        </li>

                        <li className='nav-text'>
                            <Link to='/dashboard'>
                                <AiIcons.AiOutlineForm />
                                <span>Stock</span>
                            </Link>
                        </li>
                        <br></br>
                        <h1 className='subtext'>Accounts</h1>

                        <li className='nav-text'>
                            <Link to='/accountsettings'>
                                <AiIcons.AiOutlineSetting />
                                <span>Account Settings</span>
                            </Link>
                        </li>
                        <br></br>
                        <h1 className='subtext'>Tables</h1>

                        <li className='nav-text'>
                            <Link to='/userstable'>
                                <AiIcons.AiOutlineUser />
                                <span>Users</span>
                            </Link>
                        </li>
                        
                        <li className='nav-text'>
                            <Link to='/dashboard'>
                                <AiIcons.AiFillHome />
                                <span>Produce</span>
                            </Link>
                        </li>
                        
                        <li className='nav-text'>
                            <Link to='/dashboard'>
                                <AiIcons.AiOutlineUsergroupAdd />
                                <span>Customers</span>
                            </Link>
                        </li>

                        <li className='nav-text'>
                            <Link to='/dashboard'>
                                <AiIcons.AiOutlineDropbox />
                                <span>Packaging</span>
                            </Link>
                        </li>
                    </ul>
                </nav>

            </IconContext.Provider>
        </>
    )
}

export default Navbar