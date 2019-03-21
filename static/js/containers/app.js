import axios from 'axios';
import React, { Component } from 'react';
import { Graph } from 'react-d3-graph';

const myConfig = {
    nodeHighlightBehavior: false,
    node: {
        color: '#bc2232',
        fontSize: 12,
        highlightStrokeColor: 'blue',
        labelProperty: 'name',
        size: 200,
    },
    width: 1440,
    height: 900
};

class App extends Component {

  constructor(props, context) {
    super();
    this.state = {
      data: null
    }

    this.getData()
  }

  getData() {
    axios.get('http://localhost:8080/taxonomy_graphs')
      .then(response => this.setState({data: response.data}));
  }

  render() {
    if (this.state.data === null) {
      return (
        <p>Loading...</p>
      );
    } else {
      return (
        <Graph
          id="graph-id"
          data={this.state.data}
          config={myConfig}
        />
      );
    }
  }
}

export default App;
