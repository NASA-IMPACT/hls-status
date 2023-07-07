import React from 'react';
import formatDate from '../utilities/date';
import '../styles/Alarm.css';

function Alarm({ alarm }) {


  return (
    <div className="alarm-container">
      {Object.keys(alarm).map((alarmKey) => (
        <div key={alarmKey} className="alarm-item">
          <div className="alarm-info">
            <h5 className="alarm-title">{alarmKey}</h5>
            <div className='alarm-status'>
            <div className="status-icon">
              {alarm[alarmKey].state === 'OK' ? (
                <i className="fas fa-check-circle ok-icon"></i>
              ) : alarm[alarmKey].state === 'ALARM' ? (
                <i className="fas fa-exclamation-triangle danger-icon"></i>
              ) : alarm[alarmKey].state === 'INSUFFICIENT_DATA' ? (
                <i className="fas fa-solid fa-exclamation-circle alert-icon"></i>
              ) : null}
            </div>
            <div className="alarm-details">
              <div className="alarm-state">{alarm[alarmKey].state}</div>
              <div className="alarm-timestamp">{formatDate(alarm[alarmKey].state_updated_timestamp)}</div>
            </div>
            </div>
          </div>

        </div>
      ))}
    </div>
  );
}

export default Alarm;
