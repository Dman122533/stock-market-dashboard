import plotly.graph_objects as go


def apply_chart_theme(fig):

    fig.update_layout(
        template="plotly_dark",

        height=450,

        font=dict(
            size=13
        ),

        title_font=dict(
            size=20
        ),

        xaxis=dict(
            showgrid=False
        ),

        yaxis=dict(
            showgrid=True
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=40
        )
    )

    return fig