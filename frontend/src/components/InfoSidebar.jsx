import React from 'react';
import { Shield, Heart, DollarSign, Building, Percent } from 'lucide-react';

const PLAN_DETAILS = {
  'Plan Base': {
    name: 'Plan Base',
    color: '#0F52BA',
    cobertura: 'Excluye Oftalmología y Dermatología. Cubre el resto.',
    copagoGeneral: '$15 USD',
    copagoEspecialidad: '$30 USD',
    reembolso: 'No permite reembolsos (0%)',
    hospitales: ['Hospital Central (Económico)', 'Clínica San José']
  },
  'Plan Premium': {
    name: 'Plan Premium',
    color: '#028090',
    cobertura: 'Cubre todas las especialidades médicas sin excepciones.',
    copagoGeneral: '$5 USD',
    copagoEspecialidad: '$10 USD',
    reembolso: '70% de reembolso fuera de red',
    hospitales: ['Hospital Los Ángeles (Premium)', 'Hospital Central']
  },
  'Plan Platino': {
    name: 'Plan Platino',
    color: '#00A896',
    cobertura: 'Cubre absolutamente todas las especialidades.',
    copagoGeneral: '$0 USD (Sin costo)',
    copagoEspecialidad: '$5 USD',
    reembolso: '100% de reembolso fuera de red',
    hospitales: ['Clínica VIP Internacional', 'Hospital Los Ángeles', 'Hospital Central']
  }
};

const InfoSidebar = ({ selectedPlan }) => {
  const plan = PLAN_DETAILS[selectedPlan] || PLAN_DETAILS['Plan Base'];

  return (
    <div className="info-sidebar">
      <h3 className="sidebar-title">
        <Shield size={20} className="sidebar-title-icon" style={{ color: plan.color }} />
        Detalles del Seguro
      </h3>
      
      <div className="plan-info-card">
        <div className="plan-info-header">
          <span className="plan-name-tag" style={{ color: plan.color }}>{plan.name}</span>
          <span className="plan-status-badge">Activo</span>
        </div>
        
        <div className="benefit-item">
          <span className="benefit-label">
            <Heart size={18} style={{ marginRight: '8px', verticalAlign: 'middle', color: '#EC4899' }} />
            Coberturas:
          </span>
          <span className="benefit-val" style={{ textAlign: 'right', display: 'block', maxWidth: '180px' }}>
            {plan.cobertura}
          </span>
        </div>

        <div className="benefit-item">
          <span className="benefit-label">
            <DollarSign size={18} style={{ marginRight: '8px', verticalAlign: 'middle', color: '#10B981' }} />
            Consulta General:
          </span>
          <span className="benefit-val">{plan.copagoGeneral}</span>
        </div>

        <div className="benefit-item">
          <span className="benefit-label">
            <DollarSign size={18} style={{ marginRight: '8px', verticalAlign: 'middle', color: '#3B82F6' }} />
            Especialidades:
          </span>
          <span className="benefit-val">{plan.copagoEspecialidad}</span>
        </div>

        <div className="benefit-item">
          <span className="benefit-label">
            <Percent size={18} style={{ marginRight: '8px', verticalAlign: 'middle', color: '#F59E0B' }} />
            Reembolso Fuera Red:
          </span>
          <span className="benefit-val">{plan.reembolso}</span>
        </div>
      </div>

      <h3 className="sidebar-title" style={{ marginTop: '0.5rem' }}>
        <Building size={20} className="sidebar-title-icon" style={{ color: plan.color }} />
        Red de Hospitales
      </h3>

      <div className="hospital-list">
        {plan.hospitales.map((hospital, index) => (
          <div 
            key={index} 
            className="hospital-card"
          >
            <span style={{ fontSize: '1.2rem' }}>🏥</span>
            {hospital}
          </div>
        ))}
      </div>
    </div>
  );
};

export default InfoSidebar;
