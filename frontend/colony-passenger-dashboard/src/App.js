import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Card, ListGroup } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

const API_BASE_URL = "http://localhost:8000"; // Replace with your API server address

function App() {
  const [colonies, setColonies] = useState([]);
  const [passengers, setPassengers] = useState([]);

  useEffect(() => {
    fetchColonies();
    fetchPassengers();
  }, []);

  const fetchColonies = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/colonies`);
      setColonies(response.data);
    } catch (error) {
      console.error("Error fetching colonies:", error);
    }
  };

  const fetchPassengers = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/passengers`);
      setPassengers(response.data);
    } catch (error) {
      console.error("Error fetching passengers:", error);
    }
  };

  // Add more functions to interact with other endpoints here

  return (
    <div className="App">
      <header>
        <h1>Colony & Passenger Dashboard</h1>
      </header>
      <Container>
        <Row>
          <Col>
            <Card>
              <Card.Header>Colonies</Card.Header>
              <ListGroup variant="flush">
                {colonies.map((colony) => (
                  <ListGroup.Item key={colony.id}>{colony.name}</ListGroup.Item>
                ))}
              </ListGroup>
            </Card>
          </Col>
          <Col>
            <Card>
              <Card.Header>Passengers</Card.Header>
              <ListGroup variant="flush">
                {passengers.map((passenger) => (
                  <ListGroup.Item key={passenger.id}>{passenger.name}</ListGroup.Item>
                ))}
              </ListGroup>
            </Card>
          </Col>
        </Row>
        {/* Add more sections for other endpoints here */}
      </Container>
    </div>
  );
}

export default App;
