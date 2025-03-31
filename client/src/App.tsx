import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Box } from '@chakra-ui/react';
import FormPage from './pages/FormPage';
import SubmissionsPage from './pages/SubmissionsPage';
import Navbar from './components/Navbar';

function App() {
  return (
    <Router>
      <Box minH="100vh" bg="gray.50">
        <Navbar />
        <Box as="main" pt={4}>
          <Routes>
            <Route path="/" element={<FormPage />} />
            <Route path="/submissions" element={<SubmissionsPage />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
}

export default App;
