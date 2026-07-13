import plotly.graph_objects as go


def apply_chart_theme(fig):

    fig.update_layout(
        template="plotly_dark",
        font=dict(
            size=14
        ),
        title_font=dict(
            size=20
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y= -0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    return fig