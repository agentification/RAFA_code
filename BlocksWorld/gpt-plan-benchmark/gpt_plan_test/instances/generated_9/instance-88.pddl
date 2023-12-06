

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a g)
(on b d)
(on c b)
(on d a)
(on e h)
(ontable f)
(on g e)
(ontable h)
(ontable i)
(clear c)
(clear f)
(clear i)
)
(:goal
(and
(on a g)
(on c d)
(on d f)
(on f i)
(on g h)
(on i b))
)
)


