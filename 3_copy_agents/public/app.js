function app() {
    return {
        loading: false,
        generating: false,
        reviewing: false,
        regenerating: false,
        llmProvider: 'claude',
        
        // State
        banks: [],
        selectedBank: null,
        contentDescription: '',
        wordCount: 300,
        generatedContent: '',
        availableAgents: ['compliance', 'legal', 'risk_management', 'marketing', 'customer_experience'],
        selectedReviewers: [],
        reviews: [],
        selectedFeedback: [],

        // Computed properties
        get canGenerate() {
            return !this.generating && 
                   this.selectedBank && 
                   this.contentDescription.length > 10 &&
                   this.wordCount >= 50;
        },

        get canGetFeedback() {
            return !this.reviewing && 
                   this.generatedContent.length > 0 && 
                   this.selectedReviewers.length > 0;
        },

        get canRegenerate() {
            return !this.regenerating && 
                   this.reviews.length > 0 && 
                   this.selectedFeedback.length > 0;
        },

        // Methods
        async init() {
            try {
                this.loading = true;
                const response = await fetch('/api/banks');
                const data = await response.json();
                if (data.success) {
                    this.banks = data.data;
                }
            } catch (error) {
                console.error('Error loading banks:', error);
            } finally {
                this.loading = false;
            }
        },

        async generateContent() {
            try {
                this.generating = true;
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        bankId: this.selectedBank,
                        contentDescription: this.contentDescription,
                        wordCount: this.wordCount
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    this.generatedContent = data.content;
                    this.reviews = [];
                    this.selectedFeedback = [];
                }
            } catch (error) {
                console.error('Generation failed:', error);
            } finally {
                this.generating = false;
            }
        },

        async getFeedback() {
            try {
                this.reviewing = true;
                const response = await fetch('/api/review', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        content: this.generatedContent,
                        bankId: this.selectedBank,
                        agentNames: this.selectedReviewers
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    this.reviews = data.reviews;
                    this.selectedFeedback = [];
                }
            } catch (error) {
                console.error('Feedback request failed:', error);
            } finally {
                this.reviewing = false;
            }
        },

        async regenerateContent() {
            try {
                this.regenerating = true;
                const feedbackToInclude = this.selectedFeedback
                    .map(index => this.reviews[index].feedback);
                
                const response = await fetch('/api/regenerate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        originalContent: this.generatedContent,
                        feedback: feedbackToInclude,
                        bankId: this.selectedBank
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    this.generatedContent = data.content;
                    this.selectedFeedback = [];
                }
            } catch (error) {
                console.error('Regeneration failed:', error);
            } finally {
                this.regenerating = false;
            }
        },

        toggleFeedback(index) {
            const position = this.selectedFeedback.indexOf(index);
            if (position === -1) {
                this.selectedFeedback.push(index);
            } else {
                this.selectedFeedback.splice(position, 1);
            }
        },

        async updateProvider() {
            try {
                await fetch('/api/llm-provider', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ provider: this.llmProvider })
                });
            } catch (error) {
                console.error('Failed to update provider:', error);
            }
        },

        formatFeedback(text) {
            return text.replace(/\n/g, '<br>')
                      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                      .replace(/\*(.*?)\*/g, '<em>$1</em>');
        }
    };
}
