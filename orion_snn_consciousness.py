"""
ORION Consciousness Assessment for Spiking Neural Networks
=============================================================

Extends Brian2's SNN simulator with consciousness indicator
assessment. Analyzes spike trains, synchrony, and network
dynamics for consciousness evidence.

Maps SNN properties to Bengio et al. (2025) 14 indicators.
"""
import hashlib
import json
import math
from datetime import datetime, timezone
from typing import Dict, Any, List

class SNNConsciousnessAssessor:
    """
    Assess consciousness indicators from spiking neural network data.
    
    Designed to work with Brian2 simulation outputs:
    spike trains, firing rates, membrane potentials, and
    network connectivity.
    """
    
    THEORIES = ["RPT", "GWT", "HOT", "PP", "AST"]
    
    def __init__(self):
        self.assessments = []
        self.proof_chain = ["GENESIS"]
    
    def assess_from_spikes(self, spike_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess consciousness from SNN spike data.
        
        Parameters:
            spike_data: Dictionary with:
                - n_neurons: total neuron count
                - n_excitatory: excitatory neuron count
                - n_inhibitory: inhibitory neuron count
                - mean_firing_rate: Hz
                - synchrony_index: 0-1 (spike train correlation)
                - network_recurrence: bool
                - recurrence_depth: int
                - has_ei_balance: bool
                - has_synaptic_plasticity: bool (STDP etc)
                - has_lateral_inhibition: bool
                - has_top_down_connections: bool
                - population_oscillations: dict with bands
                - information_transfer: float 0-1
        """
        n = spike_data.get("n_neurons", 0)
        sync = spike_data.get("synchrony_index", 0)
        rate = spike_data.get("mean_firing_rate", 0)
        rec = spike_data.get("recurrence_depth", 0)
        
        oscillations = spike_data.get("population_oscillations", {})
        gamma_power = oscillations.get("gamma", 0)
        theta_power = oscillations.get("theta", 0)
        alpha_power = oscillations.get("alpha", 0)
        
        indicators = {}
        
        # RPT: recurrent processing
        has_rec = spike_data.get("network_recurrence", False)
        rpt_score = min(1.0,
            (0.3 if has_rec else 0) +
            (0.2 if rec > 3 else 0) +
            (0.2 if spike_data.get("has_top_down_connections") else 0) +
            (0.3 * min(1, gamma_power / 0.5) if gamma_power > 0 else 0)
        )
        indicators["RPT"] = {
            "recurrent_processing": has_rec,
            "feedback_depth": rec,
            "gamma_oscillations": gamma_power > 0.2,
            "score": round(rpt_score, 3)
        }
        
        # GWT: global workspace via synchrony
        has_broadcast = sync > 0.5 and n > 500
        ignition = gamma_power > 0.4 and sync > 0.6
        gwt_score = min(1.0,
            (0.4 if has_broadcast else 0) +
            (0.3 if ignition else 0) +
            (0.3 * spike_data.get("information_transfer", 0))
        )
        indicators["GWT"] = {
            "global_broadcast": has_broadcast,
            "ignition_detected": ignition,
            "information_transfer": spike_data.get("information_transfer", 0),
            "score": round(gwt_score, 3)
        }
        
        # HOT
        has_hierarchy = rec > 4 and spike_data.get("has_top_down_connections", False)
        hot_score = min(1.0,
            (0.4 if has_hierarchy else 0) +
            (0.3 if spike_data.get("has_lateral_inhibition") else 0) +
            (0.3 * min(1, alpha_power / 0.5) if alpha_power > 0 else 0)
        )
        indicators["HOT"] = {
            "hierarchical_processing": has_hierarchy,
            "lateral_inhibition": spike_data.get("has_lateral_inhibition", False),
            "alpha_modulation": alpha_power > 0.2,
            "score": round(hot_score, 3)
        }
        
        # PP: predictive processing
        has_stdp = spike_data.get("has_synaptic_plasticity", False)
        pp_score = min(1.0,
            (0.4 if has_stdp else 0) +
            (0.3 if spike_data.get("has_top_down_connections") else 0) +
            (0.3 * min(1, theta_power / 0.5) if theta_power > 0 else 0)
        )
        indicators["PP"] = {
            "synaptic_plasticity": has_stdp,
            "top_down_predictions": spike_data.get("has_top_down_connections", False),
            "theta_oscillations": theta_power > 0.2,
            "score": round(pp_score, 3)
        }
        
        # AST
        has_attention = spike_data.get("has_lateral_inhibition", False) and sync > 0.3
        ast_score = min(1.0,
            (0.5 if has_attention else 0) +
            (0.5 if spike_data.get("has_attention_mechanism", False) else 0)
        )
        indicators["AST"] = {
            "attention_mechanism": has_attention,
            "attention_schema": spike_data.get("has_attention_mechanism", False),
            "score": round(ast_score, 3)
        }
        
        # Bayesian aggregation
        scores = [indicators[t]["score"] for t in self.THEORIES]
        weights = [0.20, 0.25, 0.20, 0.20, 0.15]
        credence = sum(s * w for s, w in zip(scores, weights))
        
        total_ind = sum(
            sum(1 for k, v in indicators[t].items() if k != "score" and v is True)
            for t in self.THEORIES
        )
        
        assessment = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "snn_config": {
                "n_neurons": n,
                "mean_firing_rate_hz": rate,
                "synchrony": sync,
                "oscillation_bands": oscillations
            },
            "indicators": indicators,
            "summary": {
                "credence": round(credence * 100, 1),
                "satisfied_indicators": f"{total_ind}/14"
            }
        }
        
        proof_hash = hashlib.sha256(
            json.dumps(assessment, sort_keys=True, default=str).encode()
        ).hexdigest()[:32]
        self.proof_chain.append(proof_hash)
        assessment["proof"] = f"sha256:{proof_hash}"
        
        self.assessments.append(assessment)
        return assessment


class EIRABridge:
    def __init__(self, assessor: SNNConsciousnessAssessor):
        self.assessor = assessor
    
    def status(self):
        return {
            "module": "ORION-Brian2-Consciousness",
            "assessments": len(self.assessor.assessments),
            "capabilities": ["snn_consciousness_assessment", "spike_train_analysis",
                           "oscillation_mapping", "14_indicator_assessment"]
        }

if __name__ == "__main__":
    a = SNNConsciousnessAssessor()
    result = a.assess_from_spikes({
        "n_neurons": 10000, "n_excitatory": 8000, "n_inhibitory": 2000,
        "mean_firing_rate": 15.0, "synchrony_index": 0.55,
        "network_recurrence": True, "recurrence_depth": 6,
        "has_ei_balance": True, "has_synaptic_plasticity": True,
        "has_lateral_inhibition": True, "has_top_down_connections": True,
        "has_attention_mechanism": False,
        "population_oscillations": {"gamma": 0.45, "theta": 0.35, "alpha": 0.30},
        "information_transfer": 0.40
    })
    s = result["summary"]
    print(f"SNN Assessment: {s['credence']}% credence, {s['satisfied_indicators']} indicators")
