import React from 'react';
import ReactDOM from 'react-dom';
import DayPicker from 'react-day-picker';
import 'react-day-picker/lib/style.css';

class DatePicker extends React.Component {
  constructor(props) {
    super(props);

  }

  render() {
    return (
      <DayPicker />;
    );
  }
}

ReactDOM.render(<DayPicker />, document.getElementById("date-root"));

const element = <h1>Schedule</h1>;
console.log(element);
