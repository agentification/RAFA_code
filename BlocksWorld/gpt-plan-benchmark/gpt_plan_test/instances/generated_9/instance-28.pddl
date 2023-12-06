

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b f)
(on c h)
(ontable d)
(ontable e)
(on f g)
(on g c)
(ontable h)
(on i a)
(clear b)
(clear d)
(clear e)
(clear i)
)
(:goal
(and
(on a h)
(on b a)
(on c f)
(on d i)
(on g e)
(on h c))
)
)


