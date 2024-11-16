import React from 'react'
import { Route, Routes } from 'react-router-dom'
import Home from './pages/home/Home'
import Login from './pages/Login'
import SignUp from './pages/SignUp'
import Footer from './commponents/Footer'

const App = () => {
  return (
   <>
    <Routes>
      <Route path='/' element={<Home/>}/>
      <Route path='/login' element={<Login/>}/>
      <Route path='/signup' element={<SignUp/>}/>
    </Routes>
    
    <Footer/>

   </>
  )
}

export default App
