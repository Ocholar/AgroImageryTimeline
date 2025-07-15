SELECT 
    labels.ImgID,
    labels.Quality,
    metadata.Country,
    metadata.Season,
    metadata.Variety,
    metadata.PlotSize_acres,

    ROUND(
        (
            (
                metadata.BoxADryWeight / NULLIF(metadata.BoxAWidth * metadata.BoxALength, 0)
            ) +
            (
                metadata.BoxBDryWeight / NULLIF(metadata.BoxBWidth * metadata.BoxBLength, 0)
            )
        ) / 2 * NULLIF(metadata.PlotSize_acres, 0) * 4046.86, 2
    ) AS EstimatedYieldKG,

    ROUND(
        (
            (
                (
                    metadata.BoxADryWeight / NULLIF(metadata.BoxAWidth * metadata.BoxALength, 0)
                ) +
                (
                    metadata.BoxBDryWeight / NULLIF(metadata.BoxBWidth * metadata.BoxBLength, 0)
                )
            ) / 2 * 4046.86
        ), 2
    ) AS YieldPerAcre

FROM labels
JOIN metadata ON labels.ImgID = metadata.ImgID
WHERE metadata.Variety IS NOT NULL
ORDER BY YieldPerAcre DESC;
