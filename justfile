default:
    @just --list

# Run the sprite explosion bitmapped example
sprite-explosion:
    uv run python -m arcade.examples.sprite_explosion_bitmapped

# Run given python file
[no-cd]
run file:
    @uv run python {{file}}