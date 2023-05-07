Styling
=======

Trial templates don't use the standard oTree visual layout.
Rather, you define your layout from scratch.

Here is a suggested full-screen layout.
This is based on CSS flexbox.
You can find further information on how to customize it
`here <https://css-tricks.com/snippets/css/a-guide-to-flexbox/>`__.

Minimal centered layout
-----------------------

If you only have 1 piece of content you want to put in the center of the screen,
you can use the below layout.

.. code-block:: html

    <style>
        .fullscreen {
            /* 100% of the window height */
            height: 100vh;
        }

        /* vertical stack (column) */
        .center-vh {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

    </style>

    <div class="fullscreen center-vh">
        <div>
            your content goes here.
        </div>
    </div>


3x3 layout
----------

This layout lets you place main content in the center of the screen,
and to put peripheral content at any of the 4 corners or 4 edges of the screen.

Just put your content in one of the ``<div>`` elements.
``h-stack`` and ``v-stack`` elements can be nested.


.. code-block:: html

    <style>
        .fullscreen {
            /* 100% of the window height */
            height: 100vh;
        }

        /* vertical stack (column) */
        .v-stack {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        /* horizontal stack (row) */
        .h-stack {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

    </style>

    <div class="fullscreen v-stack">
        <!-- top row -->
        <div class="h-stack">
            <div></div>
            <div></div>
            <div></div>
        </div>

        <!-- middle row -->
        <div class="h-stack">
            <div></div>
            <!-- center content -->
            <div class="h-stack" style="gap: 30px">
                <div>center 1</div>
                <div>center 2</div>
            </div>
            <div></div>
        </div>

        <!-- bottom row -->
        <div class="h-stack">
            <div></div>
            <div></div>
            <div></div>
        </div>
    </div>
