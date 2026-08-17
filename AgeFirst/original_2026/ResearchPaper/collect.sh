mkdir -p ProjectNeeds && \

# --- Ainulindale/doc ---
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Ainulindale/doc/SMNNIP_equations.docx ProjectNeeds/ && \
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Ainulindale/doc/resonant_riemann_flowing_fermat.docx ProjectNeeds/ && \
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Ainulindale/doc/cover_v2.docx ProjectNeeds/ && \
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Ainulindale/doc/addendum_III_inversion.docx ProjectNeeds/ && \
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Ainulindale/doc/outreach_challenges.docx ProjectNeeds/ && \

# --- Claude/ProofPy ---
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Claude/ProofPy/smnnip_derivation_pure.py ProjectNeeds/ && \
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Claude/ProofPy/smnnip_lagrangian_pure.py ProjectNeeds/ && \
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Claude/ProofPy/smnnip_proof_engine_console.py ProjectNeeds/ && \

# --- Claude/ProofPyTf ---
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Claude/ProofPyTf/smnnip_derivation_tf.py ProjectNeeds/ && \
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Claude/ProofPyTf/smnnip_lagrangian_tf.py ProjectNeeds/ && \
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Claude/ProofPyTf/SMNNIP_Ainulindale_Conclusion.txt ProjectNeeds/ && \

# --- Support ---
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Support/SESSION_PRIMER_SMNNIP.txt ProjectNeeds/ && \
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Support/proposed-analogous-UFT.txt ProjectNeeds/ && \
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/FirstAge/Support/outreach_challenges.txt ProjectNeeds/ && \

# --- FirstDraft ---
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/Ainulindale_Conjecture_Revised.docx ProjectNeeds/ && \
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/Cover_Page.docx ProjectNeeds/ && \
cp /home/rendier/Projects/SMNNT/ResearchPaper/FirstDraft/Masters_Tribute.docx ProjectNeeds/ && \

echo "Done. Contents of ProjectNeeds:" && ls -lh ProjectNeeds/
