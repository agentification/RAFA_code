

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b d)
(ontable c)
(on d a)
(on e b)
(on f i)
(on g c)
(on h f)
(ontable i)
(clear e)
(clear g)
(clear h)
)
(:goal
(and
(on a i)
(on b e)
(on c f)
(on d g)
(on f b)
(on h d)
(on i c))
)
)


