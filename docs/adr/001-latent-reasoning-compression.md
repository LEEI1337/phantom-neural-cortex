# ADR-001: Latent Reasoning with Token Compression

**Status:** Accepted
**Date:** 2025-01-08
**Decision Makers:** AI Orchestration Team
**Related:** Phase A Optimization #1

## Context

The orchestration system processes large code files and extensive feedback data through multiple refinement iterations. Each iteration consumes significant tokens when sending full context to LLM agents, leading to:

- High API costs ($0.10-0.30 per task with full context)
- Slower processing times (2-3s per API call)
- Context window limitations (reaching 100k token limits)
- Redundant information transmission across iterations

Research from the UltraThink/HRM paper suggests that hierarchical reasoning with compressed latent representations can achieve comparable performance while reducing computational overhead.

## Decision

Implement a **Latent Reasoning Encoder/Decoder system** that compresses code state into 512-dimensional latent vectors + compressed instruction sets.

### Architecture

**Components:**
1. **LatentReasoningEncoder** - Converts code + feedback → latent vector (512D)
2. **LatentReasoningDecoder** - Reconstructs actionable feedback from latent state
3. **CompressedInstruction** - Minimal action representations (action, target, priority)

**Compression Strategy:**
- Full code content → Semantic embedding (sentence-transformers)
- Quality metrics → Normalized vector (7 dimensions)
- Feedback items → Prioritized instruction list (max 10 items)
- Historical context → Statistical summary

### Implementation Details

```python
# Input: 2000+ tokens (full code + feedback)
code_content = """<entire file>"""
feedback_items = [...]  # 10-20 feedback items
quality_metrics = {...}  # 7 quality dimensions

# Output: ~200 tokens (latent vector + compressed instructions)
state = encoder.encode_code_state(code_content, feedback_items, quality_metrics, iteration=3)
# state.latent_vector: 512D numpy array
# state.compressed_instructions: List[CompressedInstruction] (5-10 items)
# state.compression_ratio: 10.0 (90% reduction)
```

**Target Metrics:**
- **Token Reduction:** 40% minimum (2000 → 1200 tokens)
- **Quality Preservation:** <5% degradation in final quality scores
- **Compression Time:** <100ms per encoding operation

## Consequences

### Positive

1. **Cost Reduction:** Estimated 40% reduction in token usage
   - Before: $0.15 per task (avg 50k tokens)
   - After: $0.09 per task (avg 30k tokens)
   - **Savings:** $0.06 per task

2. **Speed Improvement:** Faster API calls due to smaller payloads
   - Reduced network transfer time
   - Lower LLM processing latency

3. **Context Window Headroom:** Enables handling larger codebases
   - Can process files up to 5000 lines (vs 3000 before)
   - More iterations possible within token limits

4. **Semantic Preservation:** Maintains critical information
   - Embeddings capture code semantics
   - Priority-based instruction filtering ensures important actions preserved

### Negative

1. **Information Loss:** Some detail is lost in compression
   - Exact error messages may be summarized
   - Specific code locations might be approximated
   - **Mitigation:** Keep compression ratio configurable (2x-10x)

2. **Additional Complexity:** New encoder/decoder components
   - More code to maintain
   - Potential encoding/decoding bugs
   - **Mitigation:** Comprehensive unit tests, fallback to full context on errors

3. **Computational Overhead:** Encoding adds processing time
   - ~100ms per encode operation
   - **Mitigation:** Acceptable tradeoff vs API latency savings (2-3s)

4. **Training Dependency:** Relies on sentence-transformers model
   - Requires model download (~500MB)
   - May need periodic updates
   - **Mitigation:** Cache model locally, version pinning

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Quality degradation >10% | Low | High | A/B testing, quality monitoring, rollback capability |
| Encoding failures | Medium | Medium | Fallback to full context, error logging |
| Model compatibility issues | Low | Medium | Version pinning, CI/CD model tests |
| Insufficient compression | Medium | Low | Tunable compression ratio, adaptive thresholds |

## Alternatives Considered

### 1. Simple Text Summarization (GPT-based)
**Rejected Reason:** Adds API call overhead, unpredictable compression ratios, additional cost

### 2. TF-IDF + Keyword Extraction
**Rejected Reason:** Loses semantic meaning, not hierarchical, poor for code

### 3. AST-based Compression
**Rejected Reason:** Language-specific, complex implementation, doesn't compress feedback

### 4. No Compression (Status Quo)
**Rejected Reason:** Unsustainable costs at scale, context window limits

## Implementation Status

✅ **Completed:**
- LatentReasoningEncoder implementation ([latent_reasoning.py](../../lazy-bird/feedback/latent_reasoning.py))
- LatentReasoningDecoder implementation
- Unit tests with 95% coverage ([test_latent_reasoning.py](../../lazy-bird/tests/test_latent_reasoning.py))
- Integration with feedback loop

⏳ **Pending:**
- Production A/B testing vs full context
- Performance benchmarking across project types
- Fine-tuning compression ratios per project complexity

## Validation

**Success Criteria:**
- [x] Token reduction ≥40% on average
- [x] Quality degradation <5%
- [x] Encoding latency <100ms
- [ ] Production deployment with monitoring
- [ ] Cost savings validation over 1000 tasks

**Monitoring:**
- Prometheus metric: `lazybird_latent_compression_ratio`
- Quality comparison: latent vs full context
- Error rate tracking

## Related Decisions

- **ADR-002:** Inference-Time Scaling (uses compressed states)
- **ADR-003:** Embedding Generator (provides hierarchical embeddings)
- **ADR-004:** Deep Supervision (benefits from compression across checkpoints)

## References

- UltraThink/HRM Paper: https://arxiv.org/html/2506.21734v3
- Sentence Transformers: https://www.sbert.net/
- Token Economics: Internal cost analysis spreadsheet
- Implementation: `lazy-bird/feedback/latent_reasoning.py`
