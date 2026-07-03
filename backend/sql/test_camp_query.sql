SELECT
    offer.id, offer.candidate_no, offer.accepted, app.first_choice, app.first_choice_screening_score,
    app.second_choice, app.second_choice_screening_score, app.second_choice_screening_submitted_at,
    (CASE
        WHEN %s::BOOLEAN THEN TRUE
        WHEN NULLIF(BTRIM(COALESCE(app.first_choice, '')), '') = ANY(%s)
             AND app.first_choice_screening_score >= 80 THEN TRUE
        WHEN NULLIF(BTRIM(COALESCE(app.second_choice, '')), '') = ANY(%s)
             AND app.second_choice_screening_score >= 80
             AND (
               NULLIF(BTRIM(COALESCE(app.first_choice, '')), '')
                 = NULLIF(BTRIM(COALESCE(app.second_choice, '')), '')
               OR (
                 app.second_choice_screening_submitted_at IS NOT NULL
                 AND app.second_choice_screening_score >= 80
               )
             ) THEN TRUE
        ELSE FALSE
      END) AS can_change_accepted
FROM dtlms_plan_offer offer
LEFT JOIN LATERAL (
    SELECT id, candidate_no, first_choice, first_choice_screening_score,
           second_choice, second_choice_screening_score, second_choice_screening_submitted_at,
           is_deleted
    FROM dtlms_recruitment_applications app2
    WHERE app2.candidate_no = offer.candidate_no AND app2.is_deleted = FALSE
    ORDER BY app2.id DESC
    LIMIT 1
) app ON TRUE
LIMIT 5